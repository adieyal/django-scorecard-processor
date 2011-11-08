# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'OperationArgument.order'
        db.delete_column('scorecard_processor_operationargument', 'order')

        # Adding field 'OperationArgument.position'
        db.add_column('scorecard_processor_operationargument', 'position', self.gf('django.db.models.fields.IntegerField')(default=1), keep_default=False)


    def backwards(self, orm):
        
        # User chose to not deal with backwards NULL issues for 'OperationArgument.order'
        raise RuntimeError("Cannot reverse this migration. 'OperationArgument.order' and its values cannot be restored.")

        # Deleting field 'OperationArgument.position'
        db.delete_column('scorecard_processor_operationargument', 'position')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scorecard_processor.dataseries': {
            'Meta': {'ordering': "('-group', '-name')", 'object_name': 'DataSeries'},
            'group': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scorecard_processor.entity': {
            'Meta': {'object_name': 'Entity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scorecard_processor.operation': {
            'Meta': {'object_name': 'Operation'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_data_series': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scorecard_processor.DataSeries']", 'symmetrical': 'False'}),
            'method': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'scorecard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Scorecard']"})
        },
        'scorecard_processor.operationargument': {
            'Meta': {'ordering': "('position',)", 'object_name': 'OperationArgument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'instance_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Operation']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        },
        'scorecard_processor.question': {
            'Meta': {'object_name': 'Question'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        },
        'scorecard_processor.response': {
            'Meta': {'object_name': 'Response'},
            'baseline': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Question']"}),
            'response_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.ResponseSet']"}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'scorecard_processor.responseset': {
            'Meta': {'object_name': 'ResponseSet'},
            'data_series': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scorecard_processor.DataSeries']", 'symmetrical': 'False'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'respondant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        },
        'scorecard_processor.scorecard': {
            'Meta': {'object_name': 'Scorecard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        },
        'scorecard_processor.survey': {
            'Meta': {'object_name': 'Survey'},
            'data_series': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scorecard_processor.DataSeries']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['scorecard_processor']
