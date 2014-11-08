# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

from django.forms.widgets import TextInput

try:
    from django.utils.html import format_html
except ImportError:
    from django.utils.html import conditional_escape, mark_safe

    def format_html(format_string, *args, **kwargs):
        """
        Similar to str.format, but passes all arguments through conditional_escape,
        and calls 'mark_safe' on the result. This function should be used instead
        of str.format or % interpolation to build up small HTML fragments.
        """
        args_safe = map(conditional_escape, args)
        kwargs_safe = dict((k, conditional_escape(v)) for (k, v) in six.iteritems(kwargs))
        return mark_safe(format_string.format(*args_safe, **kwargs_safe))


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

    def __init__(self, lat_field, lon_field, attrs=None):
        attrs = {} if attrs is None else attrs.copy()
        attrs.update({
            'data-lat-field': lat_field,
            'data-lon-field': lon_field,
        })
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
