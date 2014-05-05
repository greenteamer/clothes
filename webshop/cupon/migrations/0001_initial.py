# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cupon'
        db.create_table('cupon_cupon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('percent', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('cupon', ['Cupon'])


    def backwards(self, orm):
        # Deleting model 'Cupon'
        db.delete_table('cupon_cupon')


    models = {
        'cupon.cupon': {
            'Meta': {'object_name': 'Cupon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'percent': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['cupon']