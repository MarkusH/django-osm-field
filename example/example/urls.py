# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from .views import create_view, delete_view, detail_view, list_view, update_view

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", list_view, name="list"),
    path("create/", create_view, name="create"),
    path("<int:pk>/", detail_view, name="detail"),
    path("<int:pk>/delete/", delete_view, name="delete"),
    path("<int:pk>/update/", update_view, name="update"),
]

# urlpatterns += staticfiles_urlpatterns()
