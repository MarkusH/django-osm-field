# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.fields import TextField, FloatField
from django.utils.encoding import force_text, python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .forms import OSMWidget


def validate_latitude(value):
    if value < -90 or value > 90:
        raise ValidationError('invalid latitude')


def validate_longitude(value):
    if value < -180 or value > 180:
        raise ValidationError('invalid longitude')


@python_2_unicode_compatible
class Location(object):

    def __init__(self, lat, lon, text):
        self.lat = lat
        self.lon = lon
        self.text = text

    def __str__(self):
        out = []
        if not self.text is None:
            out.append(self.text)
        if not (self.lat is None or self.lon is None):
            out.append('(%f, %f)' % (self.lat, self.lon))
        return ' '.join(out) or ''

    def __repr__(self):
        return '<Location lat=%s lon=%s text=%s>' % (
            force_text(self.lat),
            force_text(self.lon),
            force_text(self.text)
        )


class LatitudeField(six.with_metaclass(models.SubfieldBase, FloatField)):

    def formfield(self, **kwargs):
        kwargs.update({
            'max_value': 90,
            'min_value': -90,
        })
        return super(LatitudeField, self).formfield(**kwargs)


class LongitudeField(six.with_metaclass(models.SubfieldBase, FloatField)):

    def formfield(self, **kwargs):
        kwargs.update({
            'max_value': 180,
            'min_value': -180,
        })
        return super(LongitudeField, self).formfield(**kwargs)


class OSMField(six.with_metaclass(models.SubfieldBase, TextField)):

    def __init__(self, *args, **kwargs):
        self.geo_blank = kwargs.pop('geo_blank', False)
        self.geo_null = kwargs.pop('geo_null', False)
        super(OSMField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        super(OSMField, self).contribute_to_class(cls, name)
        lat_name = name + "_lat"
        if not lat_name in cls._meta.fields:
            lat = LatitudeField(_('Latitude'), blank=self.geo_blank,
                null=self.geo_null, validators=[validate_latitude])
            lat.contribute_to_class(cls, lat_name)
        lon_name = name + "_lon"
        if not lon_name in cls._meta.fields:
            lon = LongitudeField(_('Longitude'), blank=self.geo_blank,
                null=self.geo_null, validators=[validate_longitude])
            lon.contribute_to_class(cls, lon_name)

        info_name = 'get_%s_info' % name
        if not hasattr(cls, info_name):
            def _func(self):
                return Location(
                    getattr(self, lat_name),
                    getattr(self, lon_name),
                    getattr(self, name),
                )
            setattr(cls, info_name, _func)

    def formfield(self, **kwargs):
        kwargs.update({
            'widget': OSMWidget,
        })
        return super(OSMField, self).formfield(**kwargs)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules(
        [],
        [
            "^osm_field\.fields\.LatitudeField",
            "^osm_field\.fields\.LongitudeField",
            "^osm_field\.fields\.OSMField",
        ])
except ImportError:
    pass
