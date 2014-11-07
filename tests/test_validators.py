# -*- coding: utf-8 -*-

import unittest

from django.core.exceptions import ValidationError
from django.utils.six import assertRaisesRegex

from osm_field.validators import validate_latitude, validate_longitude


class TestValidators(unittest.TestCase):

    def test_validate_latitude(self):
        assertRaisesRegex(self, ValidationError, 'invalid latitude', validate_latitude, 91)
        assertRaisesRegex(self, ValidationError, 'invalid latitude', validate_latitude, -91)

    def test_validate_longitude(self):
        assertRaisesRegex(self, ValidationError, 'invalid longitude', validate_longitude, 181)
        assertRaisesRegex(self, ValidationError, 'invalid longitude', validate_longitude, -181)
