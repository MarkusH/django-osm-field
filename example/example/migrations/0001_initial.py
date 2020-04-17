# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

import osm_field.fields
import osm_field.validators


class Migration(migrations.Migration):

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ExampleModel",
            fields=[
                (
                    "id",
                    models.AutoField(
                        verbose_name="ID",
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "location",
                    osm_field.fields.OSMField(
                        lat_field="location_lat", lon_field="location_lon"
                    ),
                ),
                (
                    "location_lat",
                    osm_field.fields.LatitudeField(
                        validators=[osm_field.validators.validate_latitude]
                    ),
                ),
                (
                    "location_lon",
                    osm_field.fields.LongitudeField(
                        validators=[osm_field.validators.validate_longitude]
                    ),
                ),
                (
                    "another",
                    osm_field.fields.OSMField(
                        lat_field="some_lat_field", lon_field="other_lon_field"
                    ),
                ),
                (
                    "some_lat_field",
                    osm_field.fields.LatitudeField(
                        validators=[osm_field.validators.validate_latitude]
                    ),
                ),
                (
                    "other_lon_field",
                    osm_field.fields.LongitudeField(
                        validators=[osm_field.validators.validate_longitude]
                    ),
                ),
            ],
            options={},
            bases=(models.Model,),
        ),
    ]
