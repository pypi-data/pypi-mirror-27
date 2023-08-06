from django.conf import settings

GIT_SERVER = getattr(settings, "GIT_SERVER", "")
GIT_ROOT = getattr(settings, "GIT_ROOT", "/var/lib/giteway/")
CMD_GIT = getattr(settings, "CMD_GIT", "/usr/bin/git")
CMD_CHOWN = getattr(settings, "CMD_CHOWN", "/bin/chown")
CMD_CHMOD = getattr(settings, "CMD_CHMOD", "/bin/chmod")
CMD_MV = getattr(settings, "CMD_MV", "/bin/mv")
CMD_RM = getattr(settings, "CMD_RM", "/bin/rm")
