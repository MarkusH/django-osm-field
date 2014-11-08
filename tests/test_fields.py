# -*- coding: utf-8 -*-

import unittest

import django
from django.utils.six import assertRaisesRegex

from osm_field.fields import LatitudeField, LongitudeField, OSMField
from osm_field.forms import OSMWidget
from osm_field.validators import validate_latitude, validate_longitude


def foo_validator(value):
    pass


@unittest.skipIf(django.VERSION[:2] < (1, 7),
                 "Checks have been introduced in Django 1.7")
class TestDeconstruction(unittest.TestCase):

    def test_latitude_field(self):
        field = LatitudeField()
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, 'osm_field.fields.LatitudeField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'validators': [validate_latitude]})

    def test_latitude_field_with_validator(self):
        field = LatitudeField(validators=[foo_validator])
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, 'osm_field.fields.LatitudeField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'validators': [foo_validator, validate_latitude]})

    def test_longitude_field(self):
        field = LongitudeField()
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, 'osm_field.fields.LongitudeField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'validators': [validate_longitude]})

    def test_longitude_field_with_validator(self):
        field = LongitudeField(validators=[foo_validator])
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, 'osm_field.fields.LongitudeField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {'validators': [foo_validator, validate_longitude]})

    def test_osm_field(self):
        field = OSMField()
        field.set_attributes_from_name("location")
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'location')
        self.assertEqual(path, 'osm_field.fields.OSMField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {
            'lat_field': 'location_lat',
            'lon_field': 'location_lon',
        })

    def test_osm_field_with_args(self):
        field = OSMField(lat_field='some_lat_field', lon_field='some_lon_field')
        field.set_attributes_from_name("location")
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, 'location')
        self.assertEqual(path, 'osm_field.fields.OSMField')
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {
            'lat_field': 'some_lat_field',
            'lon_field': 'some_lon_field',
        })

    def test_osm_field_raise_without_name(self):
        field = OSMField()
        assertRaisesRegex(self, TypeError, 'unsupported operand', field.deconstruct)


class TestFormFields(unittest.TestCase):

    def test_latitude_field(self):
        field = LatitudeField()
        field.set_attributes_from_name("location_lat")
        formfield = field.formfield()
        self.assertEqual(formfield.max_value, 90)
        self.assertEqual(formfield.min_value, -90)

    def test_longitude_field(self):
        field = LongitudeField()
        field.set_attributes_from_name("location_lon")
        formfield = field.formfield()
        self.assertEqual(formfield.max_value, 180)
        self.assertEqual(formfield.min_value, -180)

    def test_osm_field(self):
        field = OSMField()
        field.set_attributes_from_name("location")
        formfield = field.formfield()
        self.assertIsInstance(formfield.widget, OSMWidget)
        self.assertEqual(formfield.widget.attrs, {
            'class': 'osmfield',
            'data-lat-field': 'location_lat',
            'data-lon-field': 'location_lon',
        })

    def test_osm_field_different_names(self):
        field = OSMField(lat_field='some_lat_field', lon_field='some_lon_field')
        field.set_attributes_from_name("location")
        formfield = field.formfield()
        self.assertIsInstance(formfield.widget, OSMWidget)
        self.assertEqual(formfield.widget.attrs, {
            'class': 'osmfield',
            'data-lat-field': 'some_lat_field',
            'data-lon-field': 'some_lon_field',
        })
