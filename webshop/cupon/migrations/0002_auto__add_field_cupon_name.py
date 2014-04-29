# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Cupon.name'
        db.add_column('cupon_cupon', 'name',
                      self.gf('django.db.models.fields.CharField')(default='test_name', max_length=256),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Cupon.name'
        db.delete_column('cupon_cupon', 'name')


    models = {
        'cupon.cupon': {
            'Meta': {'object_name': 'Cupon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'percent': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['cupon']