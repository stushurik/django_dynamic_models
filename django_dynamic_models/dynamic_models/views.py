# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.db.models import DateField
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
from django.template import RequestContext
from dynamic_models.models import DynamicModel
from dynamic_models.utils import text_description_to_model, \
    create_and_migrate_migration
from dynamic_models.widgets import CalendarWidget


def index_view(request):
    models = []
    for ct in ContentType.objects.filter(app_label='dynamic_models'):
        models.append(ct.model)
    return render_to_response('../templates/index.html',
                              {'models': models},
                              context_instance=RequestContext(request)
                              )


def ajax_get_model(request, model):
    if request.is_ajax():
        ct = ContentType.objects.get(model=model)

        date_field = {}
        for field in ct.model_class()._meta.fields:
            if isinstance(field, DateField):
                date_field[field.name] = CalendarWidget()

        class DynamicForm(ModelForm):
            class Meta:
                model = ct.model_class()
                widgets = date_field

        DynamicFormSet = modelformset_factory(
            ct.model_class(),
            form=DynamicForm,
            extra=1)

        if request.POST:

            formset = DynamicFormSet(request.POST)
            if formset.is_valid():
                print 'valid'
                formset.save()

        else:
            formset = DynamicFormSet(
                queryset=ct.model_class().objects.all()
            )

        print formset
        return render_to_response('../templates/table.html',
                                  {'formset': formset,
                                   'model': model
                                   })
    else:
        return HttpResponseRedirect(reverse('index'))


def generate(request):

    import dynamic_models.models
    for dm in DynamicModel.objects.filter(is_created=False):

        text_description_to_model(
            dynamic_models.models,
            dm.description,
            'dynamic_models'
        )

        create_and_migrate_migration()

        dm.is_created = True
        dm.save()

    return HttpResponseRedirect(reverse('index'))