from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from settings import settings

admin.autodiscover()

urlpatterns = patterns("django.views", url(r"static/(?P<path>.*)$", "static.serve",
                                            {"document_root": settings.STATIC_ROOT}), )

urlpatterns += patterns("django.views", url(r"media/(?P<path>.*)$", "static.serve",
                                            {"document_root": settings.MEDIA_ROOT}), )
urlpatterns += patterns('',
    # Example:
    # (r'^django_dynamic_models/', include('django_dynamic_models.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    (r'^', include('dynamic_models.urls')),
)


