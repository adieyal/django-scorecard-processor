# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ExcelFile'
        db.create_table('ierg_results_excelfile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('excel_file', self.gf('django.db.models.fields.files.FileField')(max_length=255)),
            ('parse_log', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('uploaded', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('ierg_results', ['ExcelFile'])


    def backwards(self, orm):
        # Deleting model 'ExcelFile'
        db.delete_table('ierg_results_excelfile')


    models = {
        'ierg_results.excelfile': {
            'Meta': {'ordering': "['-uploaded']", 'object_name': 'ExcelFile'},
            'excel_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parse_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['ierg_results']