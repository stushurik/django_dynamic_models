from django.conf.urls.defaults import *
from dynamic_models.views import index_view

urlpatterns = patterns('dynamic_models.views',
    # Example:
    # (r'^django_dynamic_models/', include('django_dynamic_models.foo.urls')),

    url(r'^', 'index_view', name='index'),
)