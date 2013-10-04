from django.conf.urls.defaults import *
urlpatterns = patterns('dynamic_models.views',
    # Example:
    # (r'^django_dynamic_models/', include('django_dynamic_models.foo.urls')),

    url(r'^$', 'index_view', name='index'),
    url(r'^generate/$', 'generate', name='generate'),
    url(r'^models/(?P<model>\w+)/$', 'ajax_get_model', name='ajax_get_model'),
)