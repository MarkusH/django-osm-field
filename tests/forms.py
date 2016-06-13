from django import forms

from .models import (
    ChildModel, CustomNamingModel, DefaultNamingModel, MixedNamingModel,
    MultipleNamingModel, ParentModel,
)

from osm_field.forms import OSMFormMixin


class CustomNamingForm(forms.ModelForm):

    class Meta:
        fields = ('location', 'latitude', 'longitude', )
        model = CustomNamingModel


class DefaultNamingForm(forms.ModelForm):

    class Meta:
        fields = ('location', 'location_lat', 'location_lon', )
        model = DefaultNamingModel


class MixedNamingForm(forms.ModelForm):

    class Meta:
        fields = ('location', 'location_lat', 'longitude', )
        model = MixedNamingModel


class MultipleNamingForm(forms.ModelForm):

    class Meta:
        fields = (
            'default_location', 'default_location_lat', 'default_location_lon',
            'custom_location', 'custom_latitude', 'custom_longitude',
        )
        model = MultipleNamingModel


class ChildModelInlineForm(OSMFormMixin, forms.ModelForm):
    class Meta:
        fields = ('location', 'location_lat', 'location_lon', )
        model = ChildModel


ChildModelFormset = forms.models.inlineformset_factory(
    ParentModel, ChildModel, extra=2, form=ChildModelInlineForm,
)
