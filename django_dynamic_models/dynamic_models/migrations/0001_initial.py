# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DynamicModel'
        db.create_table(u'dynamic_models_dynamicmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_created', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'dynamic_models', ['DynamicModel'])


    def backwards(self, orm):
        # Deleting model 'DynamicModel'
        db.delete_table(u'dynamic_models_dynamicmodel')


    models = {
        u'dynamic_models.dynamicmodel': {
            'Meta': {'object_name': 'DynamicModel'},
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_created': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['dynamic_models']