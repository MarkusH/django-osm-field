from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .views import create_view, delete_view, detail_view, list_view, update_view

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r"^$", list_view, name="list"),
    url(r"^create/$", create_view, name="create"),
    url(r"^(?P<pk>\d+)/$", detail_view, name="detail"),
    url(r"^(?P<pk>\d+)/delete/$", delete_view, name="delete"),
    url(r"^(?P<pk>\d+)/update/$", update_view, name="update"),
]

urlpatterns += staticfiles_urlpatterns()
