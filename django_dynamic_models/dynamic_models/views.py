# Create your views here.
import os
import subprocess
import yaml
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db.models import Model, IntegerField, DateField, CharField
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.forms.models import modelformset_factory
import time
from dynamic_models.models import DynamicModel


def index_view(request):
    models = []
    for ct in ContentType.objects.all():
        print ct.model
        print ct.model_class()
        print ct.app_label
        print ct.name


#dynamicmodel
#<class 'dynamic_models.models.DynamicModel'>
#dynamic_models
#dynamic model

        models.append(ct.model)

    #print models
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

        print

        formset = DynamicFormSet(
            queryset=ct.model_class().objects.all()
        )

        return render_to_response('../templates/table.html',
                                  {'formset': formset})
    else:
        return HttpResponseRedirect(reverse('index'))


def field_by_type(field_type, verbose_name=''):
    if field_type == 'int':
        return IntegerField(verbose_name=verbose_name)
    elif field_type == 'date':
        return DateField(verbose_name=verbose_name)
    elif field_type == 'char':
        return CharField(max_length=255, verbose_name=verbose_name)
    else:
        return None


def generate(request):

    import dynamic_models.models
    for dm in DynamicModel.objects.filter(is_created=False):
        dct = yaml.load(dm.description)

        for model_name in dct.keys():
            fields = dct[model_name]['fields']
            attrs = {}

            for field in fields:
                attrs[field['id']] = field_by_type(field['type'], field['title'])

            attrs['__module__'] = dynamic_models.models.__name__

            model_name = str(model_name).capitalize()
            NewModel = type(model_name, (Model,), attrs)

            setattr(dynamic_models.models, model_name, NewModel)

            new_ct = ContentType()
            new_ct.app_label = 'dynamic_models'
            new_ct.name = model_name
            new_ct.model = model_name.lower()
            new_ct.save()

    print "call_command('schemamigration', 'dynamic_models', auto=True)\n"
    call_command('schemamigration', 'dynamic_models', auto=True)

    #call_command('migrate', 'dynamic_models', settings='settings.settings')
    subprocess.call(['python', 'manage.py', 'migrate'])
        #dm.is_created = True
        #dm.save()

    #for dict in dicts:
    #    print dict.keys()

    return HttpResponseRedirect(reverse('index'))