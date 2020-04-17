# -*- coding: utf-8 -*-

import django
from django.test import SimpleTestCase
from django.test.utils import override_settings

from .forms import (
    ChildModelFormset,
    CustomNamingForm,
    DefaultNamingForm,
    FieldWidgetWithClassNameForm,
    MixedNamingForm,
    MultipleNamingForm,
    WidgetsWidgetWithClassNameForm,
    WithDataForm,
)


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
            "</script>",
            html,
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
            "</script>",
            html,
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
            "</script>",
            html,
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
            "</script>",
            html,
        )
        self.assertIn('name="custom_location"', html)
        self.assertIn('data-lat-field="custom_latitude"', html)
        self.assertIn('data-lon-field="custom_longitude"', html)
        self.assertIn('name="custom_latitude"', html)
        self.assertIn('name="custom_longitude"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_custom_location").osmfield();});'
            "</script>",
            html,
        )

    def test_field_widget_contains_class(self):
        html = FieldWidgetWithClassNameForm().as_p()
        self.assertIn('class="custom-class osmfield"', html)

    def test_widgets_widget_contains_class(self):
        html = WidgetsWidgetWithClassNameForm().as_p()
        self.assertIn('class="custom-class osmfield"', html)

    def test_widget_prefix_in_formset(self):
        html = ChildModelFormset().as_p()
        # Check for form 0
        self.assertIn('id="id_children-0-location"', html)
        self.assertIn('name="children-0-location"', html)
        self.assertIn('data-lat-field="children-0-location_lat"', html)
        self.assertIn('data-lon-field="children-0-location_lon"', html)
        self.assertIn('id="id_children-0-location_lat"', html)
        self.assertIn('id="id_children-0-location_lon"', html)
        self.assertIn('name="children-0-location_lat"', html)
        self.assertIn('name="children-0-location_lon"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_children-0-location").osmfield();});'
            "</script>",
            html,
        )
        # Check for form 1
        self.assertIn('id="id_children-1-location"', html)
        self.assertIn('name="children-1-location"', html)
        self.assertIn('data-lat-field="children-1-location_lat"', html)
        self.assertIn('data-lon-field="children-1-location_lon"', html)
        self.assertIn('id="id_children-1-location_lat"', html)
        self.assertIn('id="id_children-1-location_lon"', html)
        self.assertIn('name="children-1-location_lat"', html)
        self.assertIn('name="children-1-location_lon"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_children-1-location").osmfield();});'
            "</script>",
            html,
        )

    def test_widget_location_data_field(self):
        html = WithDataForm().as_p()
        self.assertIn('name="location"', html)
        self.assertIn('data-lat-field="latitude"', html)
        self.assertIn('data-lon-field="longitude"', html)
        self.assertIn('data-data-field="location_data"', html)
        self.assertIn('name="latitude"', html)
        self.assertIn('name="longitude"', html)
        self.assertIn('name="location_data"', html)
        self.assertIn(
            '<script type="application/javascript">'
            '$(function(){$("#id_location").osmfield();});'
            "</script>",
            html,
        )


class TestMedia(SimpleTestCase):
    @override_settings(DEBUG=True)
    def test_css_debug(self):
        css = DefaultNamingForm().media.render_css()
        self.assertIn(
            '<link href="css/vendor/leaflet.css" type="text/css" media="screen" '
            'rel="stylesheet"',
            next(css),
        )
        self.assertIn(
            '<link href="css/osm_field.css" type="text/css" media="screen" '
            'rel="stylesheet"',
            next(css),
        )

    def test_css_no_debug(self):
        css = DefaultNamingForm().media.render_css()
        self.assertIn(
            '<link href="css/vendor/leaflet.css" type="text/css" media="screen" '
            'rel="stylesheet"',
            next(css),
        )
        self.assertIn(
            '<link href="css/osm_field.min.css" type="text/css" media="screen" '
            'rel="stylesheet"',
            next(css),
        )

    @override_settings(DEBUG=True)
    def test_js_debug(self):
        js = DefaultNamingForm().media.render_js()
        if django.VERSION[:2] >= (3, 1):
            self.assertEqual(
                '<script src="js/vendor/leaflet.js"></script>'
                '<script src="js/osm_field.js"></script>',
                "".join(js),
            )
        else:
            self.assertEqual(
                '<script type="text/javascript" src="js/vendor/leaflet.js"></script>'
                '<script type="text/javascript" src="js/osm_field.js"></script>',
                "".join(js),
            )

    def test_js_no_debug(self):
        js = DefaultNamingForm().media.render_js()
        if django.VERSION[:2] >= (3, 1):
            self.assertEqual(
                '<script src="js/vendor/leaflet.js"></script>'
                '<script src="js/osm_field.min.js"></script>',
                "".join(js),
            )
        else:
            self.assertEqual(
                '<script type="text/javascript" src="js/vendor/leaflet.js"></script>'
                '<script type="text/javascript" src="js/osm_field.min.js"></script>',
                "".join(js),
            )
