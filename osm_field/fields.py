# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core import checks
from django.db.models.fields import FieldDoesNotExist, FloatField, TextField
from django.utils.encoding import force_text, python_2_unicode_compatible

from .forms import OSMFormField
from .validators import validate_latitude, validate_longitude
from .widgets import OSMWidget


@python_2_unicode_compatible
class Location(object):
    """
    A wrapper class bundling the description of a location (``text``) and its
    geo coordinates, latitude (``lat``) and longitude (``lon``).

    :param float lat: The latitude
    :param float lon: The longitude
    :param str: The description
    """

    def __init__(self, lat, lon, text):
        self.lat = lat
        self.lon = lon
        self.text = text

    def __str__(self):
        """
        Returns a string representation of this object in the form ``text (lat,
        lon)`` where either ``text`` or ``(lat, lon)'`` or both can be empty. In
        that case the return value is ``''``.
        """
        out = []
        if self.text is not None:
            out.append(self.text)
        if self.lat is not None and self.lon is not None:
            out.append('(%.6f, %.6f)' % (self.lat, self.lon))
        return ' '.join(out)

    def __repr__(self):
        return '<Location lat=%.6f lon=%.6f text=%s>' % (
            self.lat, self.lon, force_text(self.text)
        )

    def __copy__(self):
        return self.__class__(self.lat, self.lon, self.text)

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.lat == other.lat and
            self.lon == other.lon and
            self.text == other.text
        )

    def __ne__(self, other):
        return not (self == other)


class LatitudeField(FloatField):
    """
    Bases: :class:`django.db.models.FloatField`

    All :ref:`default field options <django:common-model-field-options>`.

    The ``validators`` parameter will be appended with
    :func:`~validate_latitude` if not already present.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [])
        if validate_latitude not in kwargs['validators']:
            kwargs['validators'].append(validate_latitude)
        super(LatitudeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """
        :returns: A :class:`~django.forms.FloatField` with ``max_value`` 90 and
            ``min_value`` -90.
        """
        kwargs.update({
            'max_value': 90,
            'min_value': -90,
        })
        return super(LatitudeField, self).formfield(**kwargs)


class LongitudeField(FloatField):
    """
    Bases: :class:`django.db.models.FloatField`

    All :ref:`default field options <django:common-model-field-options>`.

    The ``validators`` parameter will be appended with
    :func:`~validate_longitude` if not already present.
    """

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('validators', [])
        if validate_longitude not in kwargs['validators']:
            kwargs['validators'].append(validate_longitude)
        super(LongitudeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        """
        :returns: A :class:`~django.forms.FloatField` with ``max_value`` 180 and
            ``min_value`` -180.
        """
        kwargs.update({
            'max_value': 180,
            'min_value': -180,
        })
        return super(LongitudeField, self).formfield(**kwargs)


class OSMField(TextField):
    """
    Bases: :class:`django.db.models.TextField`

    :param str lat_field: The name of the latitude field. ``None`` (and thus
        standard behavior) by default.
    :param str lon_field: The name of the longitude field. ``None`` (and thus
        standard behavior) by default.

    All :ref:`default field options <django:common-model-field-options>`.
    """

    def __init__(self, *args, **kwargs):
        self._lat_field_name = kwargs.pop('lat_field', None)
        self._lon_field_name = kwargs.pop('lon_field', None)
        self.data_field_name = kwargs.pop('data_field', None)
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
        """
        :returns: A :class:`~osm_field.forms.OSMFormField` with a
            :class:`~osm_field.widgets.OSMWidget`.
        """
        widget_kwargs = {
            'lat_field': self.latitude_field_name,
            'lon_field': self.longitude_field_name,
        }

        if self.data_field_name:
            widget_kwargs['data_field'] = self.data_field_name

        defaults = {
            'form_class': OSMFormField,
            'widget': OSMWidget(**widget_kwargs),
        }
        defaults.update(kwargs)

        return super(OSMField, self).formfield(**defaults)

    @property
    def latitude_field_name(self):
        """
        The name of the related :class:`LatitudeField`.
        """
        if self._lat_field_name is None:
            self._lat_field_name = self.name + '_lat'
        return self._lat_field_name

    @property
    def longitude_field_name(self):
        """
        The name of the related :class:`LongitudeField`.
        """
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
