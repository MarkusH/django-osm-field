from django.db import models

from osm_field.fields import LatitudeField, LongitudeField, OSMField


class CustomNamingModel(models.Model):
    location = OSMField(lat_field="latitude", lon_field="longitude")
    latitude = LatitudeField()
    longitude = LongitudeField()


class DefaultNamingModel(models.Model):
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()


class MixedNamingModel(models.Model):
    location = OSMField(lon_field="longitude")
    location_lat = LatitudeField()
    longitude = LongitudeField()


class MultipleNamingModel(models.Model):
    default_location = OSMField()
    default_location_lat = LatitudeField()
    default_location_lon = LongitudeField()

    custom_location = OSMField(
        lat_field="custom_latitude", lon_field="custom_longitude"
    )
    custom_latitude = LatitudeField()
    custom_longitude = LongitudeField()


class LocationWithDataModel(models.Model):
    location = OSMField(
        lat_field="latitude", lon_field="longitude", data_field="location_data"
    )
    latitude = LatitudeField()
    longitude = LongitudeField()
    location_data = models.TextField()


class ParentModel(models.Model):
    name = models.CharField(max_length=31)


class ChildModel(models.Model):
    parent = models.ForeignKey(
        ParentModel, related_name="children", on_delete=models.CASCADE
    )
    location = OSMField()
    location_lat = LatitudeField()
    location_lon = LongitudeField()
