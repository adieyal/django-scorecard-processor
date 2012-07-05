# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Indicator.parent'
        db.add_column('ierg_results_indicator', 'parent',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sub_indicators', null=True, to=orm['ierg_results.Indicator']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Indicator.parent'
        db.delete_column('ierg_results_indicator', 'parent_id')


    models = {
        'ierg_results.country': {
            'Meta': {'ordering': "['name']", 'object_name': 'Country'},
            'flag': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'countries'", 'to': "orm['ierg_results.Region']"})
        },
        'ierg_results.excelfile': {
            'Meta': {'ordering': "['-uploaded']", 'object_name': 'ExcelFile'},
            'excel_file': ('django.db.models.fields.files.FileField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parse_log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'uploaded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'ierg_results.indicator': {
            'Meta': {'ordering': "['indicator']", 'object_name': 'Indicator'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indicator': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_indicators'", 'null': 'True', 'to': "orm['ierg_results.Indicator']"}),
            'target': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'ierg_results.region': {
            'Meta': {'ordering': "['name']", 'object_name': 'Region'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['ierg_results']