# -*- coding: utf-8 -*-

import unittest

from django.core.exceptions import ValidationError

from osm_field.validators import validate_latitude, validate_longitude


class TestValidators(unittest.TestCase):
    def test_validate_latitude(self):
        self.assertRaisesRegex(
            ValidationError, "invalid latitude", validate_latitude, 91
        )
        self.assertRaisesRegex(
            ValidationError, "invalid latitude", validate_latitude, -91
        )

    def test_validate_longitude(self):
        self.assertRaisesRegex(
            ValidationError, "invalid longitude", validate_longitude, 181
        )
        self.assertRaisesRegex(
            ValidationError, "invalid longitude", validate_longitude, -181
        )
