# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import osm_field.validators
import osm_field.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomNamingModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('location', osm_field.fields.OSMField(lat_field='latitude', lon_field='longitude')),
                ('latitude', osm_field.fields.LatitudeField(validators=[osm_field.validators.validate_latitude])),
                ('longitude', osm_field.fields.LongitudeField(validators=[osm_field.validators.validate_longitude])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DefaultNamingModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('location', osm_field.fields.OSMField(lat_field='location_lat', lon_field='location_lon')),
                ('location_lat', osm_field.fields.LatitudeField(validators=[osm_field.validators.validate_latitude])),
                ('location_lon', osm_field.fields.LongitudeField(validators=[osm_field.validators.validate_longitude])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MixedNamingModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('location', osm_field.fields.OSMField(lat_field='location_lat', lon_field='longitude')),
                ('location_lat', osm_field.fields.LatitudeField(validators=[osm_field.validators.validate_latitude])),
                ('longitude', osm_field.fields.LongitudeField(validators=[osm_field.validators.validate_longitude])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MultipleNamingModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('default_location', osm_field.fields.OSMField(lat_field='default_location_lat', lon_field='default_location_lon')),
                ('default_location_lat', osm_field.fields.LatitudeField(validators=[osm_field.validators.validate_latitude])),
                ('default_location_lon', osm_field.fields.LongitudeField(validators=[osm_field.validators.validate_longitude])),
                ('custom_location', osm_field.fields.OSMField(lat_field='custom_latitude', lon_field='custom_longitude')),
                ('custom_latitude', osm_field.fields.LatitudeField(validators=[osm_field.validators.validate_latitude])),
                ('custom_longitude', osm_field.fields.LongitudeField(validators=[osm_field.validators.validate_longitude])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
