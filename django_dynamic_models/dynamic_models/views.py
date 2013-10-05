# Create your views here.
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
from dynamic_models.models import DynamicModel
from dynamic_models.utils import text_description_to_model, \
    create_and_migrate_migration


def index_view(request):
    models = []
    for ct in ContentType.objects.filter(app_label='dynamic_models'):
        models.append(ct.model)
    return render_to_response('../templates/index.html', {'models': models})


def ajax_get_model(request, model):
    if request.is_ajax():
        ct = ContentType.objects.get(model=model)

        class DynamicForm(ModelForm):
            class Meta:
                model = ct.model_class()

        DynamicFormSet = modelformset_factory(
            ct.model_class(),
            form=DynamicForm,
            extra=2)

        formset = DynamicFormSet(
            queryset=ct.model_class().objects.all()
        )

        return render_to_response('../templates/table.html',
                                  {'formset': formset})
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