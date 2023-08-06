from pathlib import Path

from django.conf import settings
from django.contrib.sites.models import Site


def path_to_url(path):
    path = Path(path)

    if path.is_absolute():
        path = path.relative_to(Path(settings.MEDIA_ROOT).parent)

    return ('/' / path).as_posix()


def get_full_url(path):
    return ''.join(['https://', Site.objects.get_current().domain, path])
