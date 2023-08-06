import os
import subprocess
from .settings import CMD_GIT
from .settings import CMD_CHMOD
from .settings import CMD_CHOWN
from .settings import CMD_MV
from .settings import CMD_RM
from .settings import GIT_SERVER


def init_repo(name, username, root):
    ownner = "{}:{}".format(username, username)
    subprocess.run([CMD_GIT, "init", name, "--bare"], cwd=root)
    subprocess.run([CMD_CHMOD, "-R", "700", name], cwd=root)
    subprocess.run([CMD_CHOWN, "-R", ownner, name], cwd=root)
    return True


def rename_repo(old_name, new_name, root):
    subprocess.run([CMD_MV,old_name, new_name], cwd=root)
    return True


def delete_repo(name, root):
    subprocess.run([CMD_RM, "-rf", name], cwd=root)
    return True


def get_git_server(request):
    server = GIT_SERVER
    if not server:
        server = request.META.get("HTTP_HOST", "127.0.0.1").split(":")[0]
    if not server:
        server = "127.0.0.1"
    return server
