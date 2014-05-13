from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'example.views.list_view', name='list'),
    url(r'^create/$', 'example.views.create_view', name='create'),
    url(r'^(?P<pk>\d+)/$', 'example.views.detail_view', name='detail'),
    url(r'^(?P<pk>\d+)/delete/$', 'example.views.delete_view', name='delete'),
    url(r'^(?P<pk>\d+)/update/$', 'example.views.update_view', name='update'),
]

urlpatterns += staticfiles_urlpatterns()
