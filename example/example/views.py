from django.urls import reverse
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import ExampleModel


class ExampleCreateView(CreateView):
    fields = [
        "location",
        "location_lat",
        "location_lon",
        "another",
        "some_lat_field",
        "other_lon_field",
    ]
    model = ExampleModel

    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.object.pk})


create_view = ExampleCreateView.as_view()


class ExampleDeleteView(DeleteView):
    model = ExampleModel

    def get_success_url(self):
        return reverse("list")


delete_view = ExampleDeleteView.as_view()


class ExampleDetailView(DetailView):
    model = ExampleModel


detail_view = ExampleDetailView.as_view()


class ExampleListView(ListView):
    model = ExampleModel


list_view = ExampleListView.as_view()


class ExampleUpdateView(UpdateView):
    fields = [
        "location",
        "location_lat",
        "location_lon",
        "another",
        "some_lat_field",
        "other_lon_field",
    ]
    model = ExampleModel

    def get_success_url(self):
        return reverse("detail", kwargs={"pk": self.object.pk})


update_view = ExampleUpdateView.as_view()
