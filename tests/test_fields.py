# -*- coding: utf-8 -*-

import copy
from unittest import skipIf

import django
from django.db import models
from django.test import SimpleTestCase, TestCase

from osm_field.fields import LatitudeField, Location, LongitudeField, OSMField
from osm_field.validators import validate_latitude, validate_longitude
from osm_field.widgets import OSMWidget

from .models import (
    CustomNamingModel,
    DefaultNamingModel,
    MixedNamingModel,
    MultipleNamingModel,
)

try:
    from django.core.checks import Error
except ImportError:
    pass


def foo_validator(value):
    pass


BERLIN = Location(lat=52.5167, lon=13.3830, text="Berlin")
NEW_YORK = Location(lat=40.7127, lon=-74.005, text="New York")


@skipIf(
    django.VERSION[:2] < (1, 7),
    "Model field deconstruction has been introduced in Django 1.7",
)
class TestDeconstruction(TestCase):
    def test_latitude_field(self):
        field = LatitudeField()
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, "osm_field.fields.LatitudeField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {"validators": [validate_latitude]})

    def test_latitude_field_with_validator(self):
        field = LatitudeField(validators=[foo_validator])
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, "osm_field.fields.LatitudeField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {"validators": [foo_validator, validate_latitude]})

    def test_longitude_field(self):
        field = LongitudeField()
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, "osm_field.fields.LongitudeField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {"validators": [validate_longitude]})

    def test_longitude_field_with_validator(self):
        field = LongitudeField(validators=[foo_validator])
        name, path, args, kwargs = field.deconstruct()
        self.assertIsNone(name)
        self.assertEqual(path, "osm_field.fields.LongitudeField")
        self.assertEqual(args, [])
        self.assertEqual(kwargs, {"validators": [foo_validator, validate_longitude]})

    def test_osm_field(self):
        field = OSMField()
        field.set_attributes_from_name("location")
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, "location")
        self.assertEqual(path, "osm_field.fields.OSMField")
        self.assertEqual(args, [])
        self.assertEqual(
            kwargs, {"lat_field": "location_lat", "lon_field": "location_lon"}
        )

    def test_osm_field_with_args(self):
        field = OSMField(lat_field="some_lat_field", lon_field="some_lon_field")
        field.set_attributes_from_name("location")
        name, path, args, kwargs = field.deconstruct()
        self.assertEqual(name, "location")
        self.assertEqual(path, "osm_field.fields.OSMField")
        self.assertEqual(args, [])
        self.assertEqual(
            kwargs, {"lat_field": "some_lat_field", "lon_field": "some_lon_field"}
        )

    def test_osm_field_raise_without_name(self):
        field = OSMField()
        self.assertRaisesRegex(TypeError, "unsupported operand", field.deconstruct)


class TestFieldChecks(TestCase):
    def setUp(self):
        # Taken from IsolatedModelsTestCase in
        # django/tests/invalid_models_tests/base.py
        from django.apps import apps

        self._old_models = apps.app_configs["tests"].models.copy()

    def tearDown(self):
        # Taken from IsolatedModelsTestCase in
        # django/tests/invalid_models_tests/base.py
        from django.apps import apps

        apps.app_configs["tests"].models = self._old_models
        apps.all_models["tests"] = self._old_models
        apps.clear_cache()

    def test_no_missing_fields(self):
        class Model(models.Model):
            location = OSMField()
            location_lat = LatitudeField()
            location_lon = LongitudeField()

        checks = []
        expected = []
        field = Model._meta.get_field("location")
        checks.extend(field.check())
        self.assertEqual(checks, expected)

    def test_missing_fields(self):
        class Model(models.Model):
            location = OSMField()

        checks = []
        field = Model._meta.get_field("location")
        expected = [
            Error(
                "The OSMField 'location' references the non-existent latitude "
                "field 'location_lat'.",
                hint=None,
                obj=field,
                id="osm_field.E001",
            ),
            Error(
                "The OSMField 'location' references the non-existent longitude "
                "field 'location_lon'.",
                hint=None,
                obj=field,
                id="osm_field.E002",
            ),
        ]
        checks.extend(field.check())
        self.assertEqual(checks, expected)

    def test_no_missing_fields_exclicitly_given(self):
        class Model(models.Model):
            location = OSMField(lat_field="latitude", lon_field="longitude")
            latitude = LatitudeField()
            longitude = LongitudeField()

        checks = []
        expected = []
        field = Model._meta.get_field("location")
        checks.extend(field.check())
        self.assertEqual(checks, expected)

    def test_missing_fields_exclicitly_given(self):
        class Model(models.Model):
            location = OSMField(lat_field="lat", lon_field="lon")

        checks = []
        field = Model._meta.get_field("location")
        expected = [
            Error(
                "The OSMField 'location' references the non-existent latitude "
                "field 'lat'.",
                hint=None,
                obj=field,
                id="osm_field.E001",
            ),
            Error(
                "The OSMField 'location' references the non-existent longitude "
                "field 'lon'.",
                hint=None,
                obj=field,
                id="osm_field.E002",
            ),
        ]
        checks.extend(field.check())
        self.assertEqual(checks, expected)


class TestFormFields(TestCase):
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
        self.assertEqual(
            formfield.widget.attrs,
            {
                "class": "osmfield",
                "data-lat-field": "location_lat",
                "data-lon-field": "location_lon",
            },
        )

    def test_osm_field_different_names(self):
        field = OSMField(lat_field="some_lat_field", lon_field="some_lon_field")
        field.set_attributes_from_name("location")
        formfield = field.formfield()
        self.assertIsInstance(formfield.widget, OSMWidget)
        self.assertEqual(
            formfield.widget.attrs,
            {
                "class": "osmfield",
                "data-lat-field": "some_lat_field",
                "data-lon-field": "some_lon_field",
            },
        )


class TestModels(TestCase):
    def test_custom_naming(self):
        item = CustomNamingModel.objects.create(
            location="Berlin", latitude=52.5167, longitude=13.383
        )
        self.assertEqual(item.get_location_info(), BERLIN)
        self.assertNotEqual(item.get_location_info(), NEW_YORK)

    def test_default_naming(self):
        item = DefaultNamingModel.objects.create(
            location="Berlin", location_lat=52.5167, location_lon=13.383
        )
        self.assertEqual(item.get_location_info(), BERLIN)
        self.assertNotEqual(item.get_location_info(), NEW_YORK)

    def test_mixed_naming(self):
        item = MixedNamingModel.objects.create(
            location="Berlin", location_lat=52.5167, longitude=13.383
        )
        self.assertEqual(item.get_location_info(), BERLIN)
        self.assertNotEqual(item.get_location_info(), NEW_YORK)

    def test_multiple_naming(self):
        item = MultipleNamingModel.objects.create(
            default_location="Berlin",
            default_location_lat=52.5167,
            default_location_lon=13.383,
            custom_location="New York",
            custom_latitude=40.7127,
            custom_longitude=-74.005,
        )
        self.assertEqual(item.get_default_location_info(), BERLIN)
        self.assertEqual(item.get_custom_location_info(), NEW_YORK)
        self.assertNotEqual(item.get_default_location_info(), NEW_YORK)
        self.assertNotEqual(item.get_custom_location_info(), BERLIN)


class TestLocation(SimpleTestCase):
    def test_compare(self):
        self.assertEqual(BERLIN, BERLIN)
        self.assertNotEqual(BERLIN, NEW_YORK)

    def test_copy(self):
        berlin_new = copy.copy(BERLIN)
        self.assertEqual(BERLIN, berlin_new)
        self.assertIsNot(BERLIN, berlin_new)

    def test_repr(self):
        self.assertEqual(
            "<Location lat=52.516700 lon=13.383000 text=Berlin>", repr(BERLIN)
        )
        self.assertEqual(
            "<Location lat=40.712700 lon=-74.005000 text=New York>", repr(NEW_YORK)
        )

    def test_string(self):
        self.assertEqual("Berlin (52.516700, 13.383000)", str(BERLIN))
        self.assertEqual("New York (40.712700, -74.005000)", str(NEW_YORK))
