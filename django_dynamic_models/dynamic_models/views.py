# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import DynamicModel
from .utils import text_description_to_model, \
    create_and_migrate_migration
from .models import get_values_from_model


def index_view(request):
    models = []
    for ct in ContentType.objects.filter(app_label='dynamic_models'):
        models.append(ct.model)
    return render_to_response('../templates/index.html',
                              {'models': models},
                              context_instance=RequestContext(request)
                              )
items = None


def ajax_get_model(request, model):

    if request.is_ajax():

        data = ""

        ct = ContentType.objects.get(model=model)
        more = request.POST.get('more')

        # print not globals()['items'] or not more

        if not globals()['items'] or not more:
            globals()['items'] = get_values_from_model(ct.model_class(), 2)
            items = globals()['items']

        if more:
            items = globals().get('items')
        else:
            yaml_data = request.POST.get('value')
            if yaml_data:
                for deserialized_object in serializers.deserialize("yaml", yaml_data):
                    # deserialized_object.object._set_pk_val(None)

                    deserialized_object.save()

        query = None
        rest = 0

        try:
            query, rest = items.next()

        except StopIteration:
            pass

        if query:
            data = serializers.serialize(
                "yaml",
                query
            )

        data += "\n- rest: %s" % rest

        return HttpResponse(
            data,
            mimetype='application/yaml'
        )

    else:
        return HttpResponseRedirect(reverse('index'))


def generate(request):

    import models
    for dm in DynamicModel.objects.filter(is_created=False):

        text_description_to_model(
            models,
            dm.description,
            'dynamic_models'
        )

        create_and_migrate_migration()

        dm.is_created = True
        dm.save()

    return HttpResponseRedirect(reverse('index'))