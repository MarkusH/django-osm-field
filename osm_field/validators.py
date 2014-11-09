# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ValidationError


def validate_latitude(value):
    """
    Validates that the given value does not exceed the range [-90, 90].

    :raises: Raises a :class:`~django.core.exceptions.ValidationError` if
        ``value`` is not within the range.
    """
    if value < -90 or value > 90:
        raise ValidationError('invalid latitude')


def validate_longitude(value):
    """
    Validates that the given value does not exceed the range [-180, 180].

    :raises: Raises a :class:`~django.core.exceptions.ValidationError` if
        ``value`` is not within the range.
    """
    if value < -180 or value > 180:
        raise ValidationError('invalid longitude')
