import os
import subprocess
from django.core.management import call_command
import yaml
from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import clear_url_caches
from django.db.models import IntegerField, DateField, CharField, Model
from django.utils.importlib import import_module
from django.conf import settings


def _field_by_type(field_type, verbose_name=''):
    if field_type == 'int':
        return IntegerField(verbose_name=verbose_name)
    elif field_type == 'date':
        return DateField(verbose_name=verbose_name)
    elif field_type == 'char':
        return CharField(max_length=255, verbose_name=verbose_name)
    else:
        return None


def text_description_to_model(module, text, app_label, admin_register=True, verbosity=False):
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

        if verbosity:
            print 'Creating %s ...' % model_name

        try:
            new_ct = ContentType()
            new_ct.app_label = app_label
            new_ct.name = model_name
            new_ct.model = model_name.lower()
            new_ct.save()

        except Exception:
            if verbosity:
                print 'ContentType %s exist' % model_name

        if admin_register:
            try:
                class Admin(admin.ModelAdmin):
                    pass

                admin.site.register(NewModel, Admin)
            except Exception:
                pass

    if admin_register:
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()


def create_and_migrate_migration():

    call_command('schemamigration', 'dynamic_models', auto=True)
    # call_command('syncdb', migrate=True)

    # subprocess.call(
    #     [
    #        'python',
    #        os.path.join(settings.DJANGO_PROJECT_ROOT, 'manage.py'),
    #        'schemamigration',
    #        'dynamic_models',
    #        '--auto'
    #     ]
    # )
    subprocess.call(
        [
            'python',
            os.path.join(settings.DJANGO_PROJECT_ROOT, 'manage.py'),
            'migrate'
        ]
    )