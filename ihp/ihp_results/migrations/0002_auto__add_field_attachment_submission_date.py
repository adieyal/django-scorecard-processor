# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Attachment.submission_date'
        db.add_column('ihp_results_attachment', 'submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2012, 3, 27, 15, 29, 32, 551074), blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Attachment.submission_date'
        db.delete_column('ihp_results_attachment', 'submission_date')


    models = {
        'ihp_results.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Entity']"}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'scorecard_processor.entity': {
            'Meta': {'ordering': "('entity_type', 'name')", 'unique_together': "(('name', 'project'),)", 'object_name': 'Entity'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.EntityType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"})
        },
        'scorecard_processor.entitytype': {
            'Meta': {'object_name': 'EntityType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'plural': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"})
        },
        'scorecard_processor.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['ihp_results']
