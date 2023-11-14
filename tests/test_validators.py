# -*- coding: utf-8 -*-

import unittest

from django.core.exceptions import ValidationError

from osm_field.validators import validate_latitude, validate_longitude


class TestValidators(unittest.TestCase):
    def test_validate_latitude(self):
        # This is quick
        for i in range(-89, 91):
            validate_latitude(i)

        validate_latitude(-89.9)
        validate_latitude(-0.1)
        validate_latitude(-0.0)
        validate_latitude(0.1)
        validate_latitude(90.0)

        self.assertRaisesRegex(
            ValidationError, "invalid latitude", validate_latitude, 91
        )
        self.assertRaisesRegex(
            ValidationError, "invalid latitude", validate_latitude, -91
        )

    def test_validate_longitude(self):
        # This is quick
        for i in range(-179, 181):
            validate_longitude(i)

        validate_longitude(-179.9)
        validate_longitude(-0.1)
        validate_longitude(-0.0)
        validate_longitude(0.1)
        validate_longitude(179.9)

        self.assertRaisesRegex(
            ValidationError, "invalid longitude", validate_longitude, 181
        )
        self.assertRaisesRegex(
            ValidationError, "invalid longitude", validate_longitude, -181
        )
