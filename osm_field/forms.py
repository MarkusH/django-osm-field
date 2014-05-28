# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.forms.widgets import TextInput
from django.utils.html import format_html


def _get_js():
    from django.conf import settings
    base = ['js/vendor/leaflet.js']
    if settings.configured and settings.DEBUG:
        base.extend(['js/osm_field.js'])
    else:
        base.extend(['js/osm_field.min.js'])
    return base


def _get_css():
    from django.conf import settings
    base = ['css/vendor/leaflet.css']
    if settings.configured and settings.DEBUG:
        base.extend(['css/osm_field.css'])
    else:
        base.extend(['css/osm_field.min.css'])
    return base


class OSMWidget(TextInput):

    class Media:
        css = {'screen': _get_css()}
        js = _get_js()

    def __init__(self, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        if 'class' in attrs:
            attrs['class'] += ' osmfield'
        else:
            attrs['class'] = 'osmfield'
        super(OSMWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        ret = super(OSMWidget, self).render(name, value, attrs=attrs)
        id_ = attrs['id']
        ret += self.render_osmfield(id_)
        return ret

    def render_osmfield(self, id_):
        # we need {{ and }} because of .format() working with {}
        return format_html('<script type="application/javascript">$(function()'
                           '{{$("#{0}").osmfield();}});</script>', id_)
