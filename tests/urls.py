from django.contrib import admin

try:
    from django.urls import include, url
except ImportError:
    from django.conf.urls import include, url

admin.autodiscover()

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
