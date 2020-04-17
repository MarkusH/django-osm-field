from django import forms

from osm_field.widgets import OSMWidget

from .models import (
    ChildModel,
    CustomNamingModel,
    DefaultNamingModel,
    LocationWithDataModel,
    MixedNamingModel,
    MultipleNamingModel,
    ParentModel,
)


class CustomNamingForm(forms.ModelForm):
    class Meta:
        fields = (
            "location",
            "latitude",
            "longitude",
        )
        model = CustomNamingModel


class DefaultNamingForm(forms.ModelForm):
    class Meta:
        fields = (
            "location",
            "location_lat",
            "location_lon",
        )
        model = DefaultNamingModel


class MixedNamingForm(forms.ModelForm):
    class Meta:
        fields = (
            "location",
            "location_lat",
            "longitude",
        )
        model = MixedNamingModel


class MultipleNamingForm(forms.ModelForm):
    class Meta:
        fields = (
            "default_location",
            "default_location_lat",
            "default_location_lon",
            "custom_location",
            "custom_latitude",
            "custom_longitude",
        )
        model = MultipleNamingModel


class FieldWidgetWithClassNameForm(forms.ModelForm):
    location = forms.CharField(
        widget=OSMWidget(
            "location_lat", "location_lon", attrs={"class": "custom-class"}
        )
    )

    class Meta:
        fields = (
            "location",
            "location_lat",
            "location_lon",
        )
        model = DefaultNamingModel


class WidgetsWidgetWithClassNameForm(forms.ModelForm):
    class Meta:
        fields = (
            "location",
            "location_lat",
            "location_lon",
        )
        model = DefaultNamingModel
        widgets = {
            "location": OSMWidget(
                "location_lat", "location_lon", attrs={"class": "custom-class"}
            ),
        }


class ChildModelInlineForm(forms.ModelForm):
    class Meta:
        fields = (
            "location",
            "location_lat",
            "location_lon",
        )
        model = ChildModel


ChildModelFormset = forms.models.inlineformset_factory(
    ParentModel, ChildModel, extra=2, form=ChildModelInlineForm,
)


class WithDataForm(forms.ModelForm):
    class Meta:
        fields = (
            "location",
            "latitude",
            "longitude",
            "location_data",
        )
        model = LocationWithDataModel
