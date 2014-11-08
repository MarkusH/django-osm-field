# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import six

try:  # noqa
    from django.core import checks
except ImportError:  # noqa: Django<1.7
    pass

from django.db import models
from django.db.models.fields import TextField, FloatField, FieldDoesNotExist
from django.utils.encoding import force_text, python_2_unicode_compatible

from .forms import OSMWidget
from .validators import validate_latitude, validate_longitude


@python_2_unicode_compatible
class Location(object):

    def __init__(self, lat, lon, text):
        self.lat = lat
        self.lon = lon
        self.text = text

    def __str__(self):
        out = []
        if self.text is not None:
            out.append(self.text)
        if self.lat is not None and self.lon is not None:
            out.append('(%f, %f)' % (self.lat, self.lon))
        return ' '.join(out) or ''

    def __repr__(self):
        return '<Location lat=%s lon=%s text=%s>' % (
            force_text(self.lat),
            force_text(self.lon),
            force_text(self.text)
        )


class LatitudeField(six.with_metaclass(models.SubfieldBase, FloatField)):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [])
        if validate_latitude not in kwargs['validators']:
            kwargs['validators'].append(validate_latitude)
        super(LatitudeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'max_value': 90,
            'min_value': -90,
        })
        return super(LatitudeField, self).formfield(**kwargs)


class LongitudeField(six.with_metaclass(models.SubfieldBase, FloatField)):

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [])
        if validate_longitude not in kwargs['validators']:
            kwargs['validators'].append(validate_longitude)
        super(LongitudeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        kwargs.update({
            'max_value': 180,
            'min_value': -180,
        })
        return super(LongitudeField, self).formfield(**kwargs)


class OSMField(six.with_metaclass(models.SubfieldBase, TextField)):

    def __init__(self, *args, **kwargs):
        self._lat_field_name = kwargs.pop('lat_field', None)
        self._lon_field_name = kwargs.pop('lon_field', None)
        super(OSMField, self).__init__(*args, **kwargs)

    def contribute_to_class(self, cls, name):
        info_name = 'get_%s_info' % name
        if not hasattr(cls, info_name):
            def _func(obj):
                return Location(
                    getattr(obj, self.latitude_field_name),
                    getattr(obj, self.longitude_field_name),
                    getattr(obj, name),
                )
            setattr(cls, info_name, _func)

        super(OSMField, self).contribute_to_class(cls, name)

    def check(self, **kwargs):
        errors = super(OSMField, self).check(**kwargs)
        errors.extend(self._check_latitude_field())
        errors.extend(self._check_longitude_field())
        return errors

    def _check_latitude_field(self):
        opts = self.model._meta
        try:
            opts.get_field(self.latitude_field_name)
        except FieldDoesNotExist:
            return [
                checks.Error(
                    "The OSMField '%s' references the non-existent latitude field '%s'." % (
                        self.name, self.latitude_field_name,
                    ),
                    hint=None,
                    obj=self,
                    id='osm_field.E001',
                )
            ]
        else:
            return []

    def _check_longitude_field(self):
        opts = self.model._meta
        try:
            opts.get_field(self.longitude_field_name)
        except FieldDoesNotExist:
            return [
                checks.Error(
                    "The OSMField '%s' references the non-existent longitude field '%s'." % (
                        self.name, self.longitude_field_name,
                    ),
                    hint=None,
                    obj=self,
                    id='osm_field.E002',
                )
            ]
        else:
            return []

    def deconstruct(self):
        name, path, args, kwargs = super(OSMField, self).deconstruct()
        kwargs.update({
            'lat_field': self.latitude_field_name,
            'lon_field': self.longitude_field_name,
        })
        return name, path, args, kwargs

    def formfield(self, **kwargs):
        widget = OSMWidget(lat_field=self.latitude_field_name,
            lon_field=self.longitude_field_name)
        kwargs.update({
            'widget': widget,
        })
        return super(OSMField, self).formfield(**kwargs)

    @property
    def latitude_field_name(self):
        if self._lat_field_name is None:
            self._lat_field_name = self.name + '_lat'
        return self._lat_field_name

    @property
    def longitude_field_name(self):
        if self._lon_field_name is None:
            self._lon_field_name = self.name + '_lon'
        return self._lon_field_name


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
