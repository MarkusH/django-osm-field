# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError


def validate_latitude(value):
    if value < -90 or value > 90:
        raise ValidationError('invalid latitude')


def validate_longitude(value):
    if value < -180 or value > 180:
        raise ValidationError('invalid longitude')
