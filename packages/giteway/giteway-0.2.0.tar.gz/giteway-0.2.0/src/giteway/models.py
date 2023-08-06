import threading
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.db.models.signals import pre_save
from django.db.models.signals import post_delete
from django_global_request.middleware import get_request
from .settings import GIT_ROOT
from .utils import init_repo
from .utils import rename_repo
from .utils import delete_repo
from .utils import get_git_server


class Repo(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, models.CASCADE, blank=True, related_name="repos", verbose_name=_("User"))
    name = models.CharField(max_length=32, unique=True, verbose_name=_("Name"))
    description = models.CharField(max_length=64, verbose_name=_("Description"))

    class Meta:
        verbose_name = _("Repo")
        verbose_name_plural = _("Repos")

    def __str__(self):
        return self.name

    def address(self):
        request = get_request()
        root = GIT_ROOT
        server = get_git_server(request)
        return "{}@{}:{}/{}/".format(self.user.username, server, root, self.name).replace("//", "/")
    address.short_description = _("Address")


repo_on_change_storage = threading.local()


def repo_on_created(**kwargs):
    created = kwargs.get("created")
    repo = kwargs.get("instance")
    if created:
        print("init repo...")
        init_repo(repo.name, repo.user.username, GIT_ROOT)
    else:
        if repo.name != repo_on_change_storage.old_repo.name:
            print("rename repo...")
            rename_repo(repo_on_change_storage.old_repo.name, repo.name, GIT_ROOT)


def repo_on_change(**kwargs):
    new_repo = kwargs.get("instance", None)
    if new_repo.pk:
        repo_on_change_storage.old_repo = Repo.objects.get(pk=new_repo.pk)

def repo_on_delete(**kwargs):
    repo = kwargs.get("instance")
    delete_repo(repo.name, GIT_ROOT)

post_save.connect(repo_on_created, sender=Repo)
pre_save.connect(repo_on_change, sender=Repo)
post_delete.connect(repo_on_delete, sender=Repo)
