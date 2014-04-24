# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.widgets import Textarea


def _get_js():
    from django.conf import settings
    if settings.configured and settings.DEBUG:
        return ('js/osm_field.js', )
    else:
        return ('js/osm_field.min.js', )


def _get_css():
    from django.conf import settings
    if settings.configured and settings.DEBUG:
        return ('css/osm_field.css', )
    else:
        return ('css/osm_field.min.css', )


class OSMWidget(Textarea):

    class Media:
        css = {'screen': _get_css()}
        js = _get_js()
