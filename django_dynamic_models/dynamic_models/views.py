# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.db.models import DateField
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
from django.template import RequestContext

from .models import DynamicModel
from .utils import text_description_to_model, \
    create_and_migrate_migration
from .widgets import CalendarWidget
from django_dynamic_models.dynamic_models.models import get_values_from_model


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

        # date_field = {}
        # for field in ct.model_class()._meta.fields:
        #     if isinstance(field, DateField):
        #         date_field[field.name] = CalendarWidget()

        # class DynamicForm(ModelForm):
        #     class Meta:
        #         model = ct.model_class()
        #         widgets = date_field

        # DynamicFormSet = modelformset_factory(
        #     ct.model_class(),
        #     form=DynamicForm,
        #     extra=1,
        #     can_delete=True,
        # )

        more = request.POST.get('more')

        items = None

        if not items or not more:
            globals()['items'] = get_values_from_model(ct.model_class(), 2)
            items = globals().get('items')

        # if True:
        #
        #     initial = """
        #         - fields: {department: '5', spots: 5}
        #           model: dynamic_models.rooms
        #           pk: -1
        #         - fields: {department: '6', spots: 6}
        #           model: dynamic_models.rooms
        #           pk: -2
        #     """
        #
        #     for deserialized_object in serializers.deserialize("yaml", initial):
        #         print dir(deserialized_object.object)
        #         deserialized_object.object._set_pk_val(None)
        #         deserialized_object.save()
        #
        # else:

        query = None

        try:
            query = items.next()

        except StopIteration:
            pass

        if query:
            data = serializers.serialize(
                "yaml",
                query,
            )

        print type(data)

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