import subprocess
import yaml
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.urlresolvers import clear_url_caches
from django.db.models import IntegerField, DateField, CharField, Model
from django.utils.importlib import import_module
from settings import settings


def _field_by_type(field_type, verbose_name=''):
    if field_type == 'int':
        return IntegerField(verbose_name=verbose_name)
    elif field_type == 'date':
        return DateField(verbose_name=verbose_name)
    elif field_type == 'char':
        return CharField(max_length=255, verbose_name=verbose_name)
    else:
        return None


def text_description_to_model(module, text, app_label, admin_register=True):
    dct = yaml.load(text)
    for model_name in dct.keys():
        fields = dct[model_name]['fields']
        attrs = {}

        for field in fields:
            attrs[field['id']] = _field_by_type(field['type'], field['title'])

        attrs['__module__'] = module.__name__

        model_name = str(model_name).capitalize()
        NewModel = type(model_name, (Model,), attrs)

        setattr(module, model_name, NewModel)

        new_ct = ContentType()
        new_ct.app_label = app_label
        new_ct.name = model_name
        new_ct.model = model_name.lower()
        new_ct.save()

        if admin_register:

            class Admin(admin.ModelAdmin):
                pass

            admin.site.register(NewModel, Admin)

    if admin_register:
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()




def create_and_migrate_migration():

    #subprocess.call(
    #    [
    #        'python',
    #        'manage.py',
    #        'schemamigration',
    #        'dynamic_models',
    #        '--auto'
    #    ])
    call_command('schemamigration', 'dynamic_models', auto=True)
    subprocess.call(
        [
            'python',
            'manage.py',
            'migrate'
        ])
    #
    #
    #
    #call_command('migrate')