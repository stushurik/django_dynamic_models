MANAGE=django-admin.py

test:
	PYTHONPATH=`pwd`:`pwd`/django_dynamic_models DJANGO_SETTINGS_MODULE=django_dynamic_models.settings.test_settings $(MANAGE) test dynamic_models

run:
	PYTHONPATH=`pwd`:`pwd`/django_dynamic_models DJANGO_SETTINGS_MODULE=django_dynamic_models.settings.settings $(MANAGE) runserver

syncdb:
    PYTHONPATH=`pwd`:`pwd`/django_dynamic_models DJANGO_SETTINGS_MODULE=django_dynamic_models.settings.settings $(MANAGE) syncdb --noinput --migrate