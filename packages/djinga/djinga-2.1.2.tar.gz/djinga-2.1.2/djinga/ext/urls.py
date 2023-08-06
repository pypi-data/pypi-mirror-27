"""
Extensions for URL reversing
"""

try:
    from django.urls import reverse
except ImportError:
    # Django 1.8
    from django.core.urlresolvers import reverse

from ._base import SimpleTag


class URLExtension(SimpleTag):
    tags = {'url'}

    def tag_func(self, name, *args, **kwargs):
        return reverse(name, args=args, kwargs=kwargs)
