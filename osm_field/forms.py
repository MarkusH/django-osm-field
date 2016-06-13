import django

# For reverse compatibility
from .widgets import OSMWidget  # flake8: noqa

try:
    from django.forms import BoundField, CharField, FloatField
except ImportError:
    from django.forms import CharField, FloatField
    from django.forms.forms import BoundField


class PrefixedBoundField(BoundField):
    """
    A bound field that passes the form's prefix into the widget's attrs
    """
    def as_widget(self, widget=None, attrs=None, only_initial=False):
        attrs = {} if attrs is None else attrs.copy()
        if self.form.prefix:
            attrs.update({
                'prefix': self.form.prefix,
            })
        return super(PrefixedBoundField, self).as_widget(widget, attrs, only_initial)


class PrefixedFormFieldMixin(object):
    """
    A form field that binds to a custom bound field class, so we can pass the
    form's prefix into the widget's attrs
    """
    def get_bound_field(self, form, field_name):
        """
        For Django 1.9+

        Return a BoundField instance that will be used when accessing the form
        field in a template.
        """
        return PrefixedBoundField(form, self, field_name)


class OSMFormField(PrefixedFormFieldMixin, CharField):
    pass


class OSMFormMixin(object):
    def __init__(self, *args, **kwargs):
        super(OSMFormMixin, self).__init__(*args, **kwargs)
        if django.VERSION < (1, 9):
            for k in self.fields:
                f = self.fields[k]
                if issubclass(f.__class__, OSMFormField):
                    f.widget.attrs['prefix'] = self.prefix
