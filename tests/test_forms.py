# -*- coding: utf-8 -*-

import sys

from django.test import SimpleTestCase
from django.test.utils import override_settings

from .forms import (CustomNamingForm, DefaultNamingForm, MixedNamingForm,
    MultipleNamingForm)


class TestWidget(SimpleTestCase):

    def test_custom_naming(self):
        html = CustomNamingForm().as_p()
        self.assertIn('name="location"', html)
        self.assertIn('data-lat-field="latitude"', html)
        self.assertIn('data-lon-field="longitude"', html)
        self.assertIn('name="latitude"', html)
        self.assertIn('name="longitude"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_location").osmfield();});'
            '</script>',
            html
        )

    def test_default_naming(self):
        html = DefaultNamingForm().as_p()
        self.assertIn('name="location"', html)
        self.assertIn('data-lat-field="location_lat"', html)
        self.assertIn('data-lon-field="location_lon"', html)
        self.assertIn('name="location_lat"', html)
        self.assertIn('name="location_lon"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_location").osmfield();});'
            '</script>',
            html
        )

    def test_mixed_naming(self):
        html = MixedNamingForm().as_p()
        self.assertIn('name="location"', html)
        self.assertIn('data-lat-field="location_lat"', html)
        self.assertIn('data-lon-field="longitude"', html)
        self.assertIn('name="location_lat"', html)
        self.assertIn('name="longitude"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_location").osmfield();});'
            '</script>',
            html
        )

    def test_multiple_naming(self):
        html = MultipleNamingForm().as_p()
        self.assertIn('name="default_location"', html)
        self.assertIn('data-lat-field="default_location_lat"', html)
        self.assertIn('data-lon-field="default_location_lon"', html)
        self.assertIn('name="default_location_lat"', html)
        self.assertIn('name="default_location_lon"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_default_location").osmfield();});'
            '</script>',
            html
        )
        self.assertIn('name="custom_location"', html)
        self.assertIn('data-lat-field="custom_latitude"', html)
        self.assertIn('data-lon-field="custom_longitude"', html)
        self.assertIn('name="custom_latitude"', html)
        self.assertIn('name="custom_longitude"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_custom_location").osmfield();});'
            '</script>',
            html
        )


class TestMedia(SimpleTestCase):

    @override_settings(DEBUG=True)
    def test_css_debug(self):
        css = DefaultNamingForm().media.render_css()
        self.assertEqual(
            '<link href="css/vendor/leaflet.css" type="text/css" media="screen" rel="stylesheet" />'
            '<link href="css/osm_field.css" type="text/css" media="screen" rel="stylesheet" />',
            ''.join(css)
        )

    def test_css_no_debug(self):
        css = DefaultNamingForm().media.render_css()
        self.assertEqual(
            '<link href="css/vendor/leaflet.css" type="text/css" media="screen" rel="stylesheet" />'
            '<link href="css/osm_field.min.css" type="text/css" media="screen" rel="stylesheet" />',
            ''.join(css)
        )

    @override_settings(DEBUG=True)
    def test_js_debug(self):
        js = DefaultNamingForm().media.render_js()
        self.assertEqual(
            '<script type="text/javascript" src="js/vendor/leaflet.js"></script>'
            '<script type="text/javascript" src="js/osm_field.js"></script>',
            ''.join(js)
        )

    def test_js_no_debug(self):
        js = DefaultNamingForm().media.render_js()
        self.assertEqual(
            '<script type="text/javascript" src="js/vendor/leaflet.js"></script>'
            '<script type="text/javascript" src="js/osm_field.min.js"></script>',
            ''.join(js)
        )
