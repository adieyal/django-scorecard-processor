# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding unique constraint on 'SurveyTranslation', fields ['lang', 'parent_object']
        db.create_unique('scorecard_processor_surveytranslation', ['lang', 'parent_object_id'])

        # Adding unique constraint on 'QuestionGroupTranslation', fields ['lang', 'parent_object']
        db.create_unique('scorecard_processor_questiongrouptranslation', ['lang', 'parent_object_id'])

        # Adding unique constraint on 'QuestionTranslation', fields ['lang', 'parent_object']
        db.create_unique('scorecard_processor_questiontranslation', ['lang', 'parent_object_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'QuestionTranslation', fields ['lang', 'parent_object']
        db.delete_unique('scorecard_processor_questiontranslation', ['lang', 'parent_object_id'])

        # Removing unique constraint on 'QuestionGroupTranslation', fields ['lang', 'parent_object']
        db.delete_unique('scorecard_processor_questiongrouptranslation', ['lang', 'parent_object_id'])

        # Removing unique constraint on 'SurveyTranslation', fields ['lang', 'parent_object']
        db.delete_unique('scorecard_processor_surveytranslation', ['lang', 'parent_object_id'])


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
            'Meta': {'ordering': "('-group', 'name')", 'object_name': 'DataSeries'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.DataSeriesGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'scorecard_processor.dataseriesgroup': {
            'Meta': {'ordering': "('name',)", 'object_name': 'DataSeriesGroup'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"}),
            'reverse_ordering': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'scorecard_processor.entity': {
            'Meta': {'ordering': "('entity_type', 'name')", 'unique_together': "(('name', 'project'),)", 'object_name': 'Entity'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'entity_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.EntityType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"}),
            'user_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'scorecard_processor.entitytype': {
            'Meta': {'object_name': 'EntityType'},
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'primary_key': 'True'}),
            'plural': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"})
        },
        'scorecard_processor.glossarydefinition': {
            'Meta': {'object_name': 'GlossaryDefinition'},
            'definition': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"})
        },
        'scorecard_processor.glossaryterm': {
            'Meta': {'object_name': 'GlossaryTerm'},
            'definition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.GlossaryDefinition']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'scorecard_processor.importfieldmap': {
            'Meta': {'object_name': 'ImportFieldMap'},
            'cell': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'field': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Question']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'importmap': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.ImportMap']"})
        },
        'scorecard_processor.importmap': {
            'Meta': {'object_name': 'ImportMap'},
            'example_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        },
        'scorecard_processor.operation': {
            'Meta': {'ordering': "('identifier',)", 'object_name': 'Operation'},
            'configuration': ('django.db.models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'indicator': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'operation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'scorecard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Scorecard']"})
        },
        'scorecard_processor.operationargument': {
            'Meta': {'ordering': "('position',)", 'unique_together': "(('position', 'operation'),)", 'object_name': 'OperationArgument'},
            'argument_extractor': ('django.db.models.fields.CharField', [], {'default': "'value'", 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'instance_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Operation']"}),
            'position': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'})
        },
        'scorecard_processor.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_set': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False'})
        },
        'scorecard_processor.question': {
            'Meta': {'ordering': "('group__ordering', 'id')", 'unique_together': "(('survey', 'identifier'),)", 'object_name': 'Question'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.QuestionGroup']", 'null': 'True', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"}),
            'validator': ('django.db.models.fields.CharField', [], {'default': "'anything'", 'max_length': '30'}),
            'widget': ('django.db.models.fields.CharField', [], {'default': "'text'", 'max_length': '30'})
        },
        'scorecard_processor.questiongroup': {
            'Meta': {'ordering': "('ordering', 'name')", 'object_name': 'QuestionGroup'},
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'ordering': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        },
        'scorecard_processor.questiongrouptranslation': {
            'Meta': {'unique_together': "(('parent_object', 'lang'),)", 'object_name': 'QuestionGroupTranslation'},
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.QuestionGroup']"})
        },
        'scorecard_processor.questiontranslation': {
            'Meta': {'unique_together': "(('parent_object', 'lang'),)", 'object_name': 'QuestionTranslation'},
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'parent_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Question']"}),
            'question': ('django.db.models.fields.TextField', [], {})
        },
        'scorecard_processor.reportrun': {
            'Meta': {'object_name': 'ReportRun'},
            'aggregate_by_entity': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aggregate_on': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.DataSeriesGroup']", 'null': 'True', 'blank': 'True'}),
            'compare_series': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'indicator_series_set'", 'null': 'True', 'to': "orm['scorecard_processor.DataSeriesGroup']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_to_dataseries': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['scorecard_processor.DataSeries']", 'null': 'True', 'blank': 'True'}),
            'limit_to_entity': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['scorecard_processor.Entity']", 'null': 'True', 'blank': 'True'}),
            'limit_to_entitytype': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['scorecard_processor.EntityType']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scorecard': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Scorecard']"})
        },
        'scorecard_processor.response': {
            'Meta': {'object_name': 'Response'},
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Question']"}),
            'respondant': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'response_set': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.ResponseSet']"}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'valid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.TextField', [], {})
        },
        'scorecard_processor.responseoverride': {
            'Meta': {'object_name': 'ResponseOverride'},
            'data_series': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scorecard_processor.DataSeries']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Question']"}),
            'value': ('django.db.models.TextField', [], {})
        },
        'scorecard_processor.responseset': {
            'Meta': {'ordering': "('-last_update',)", 'object_name': 'ResponseSet'},
            'data_series': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scorecard_processor.DataSeries']", 'symmetrical': 'False'}),
            'entity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Entity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_response_id': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'submission_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        },
        'scorecard_processor.scorecard': {
            'Meta': {'object_name': 'Scorecard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"})
        },
        'scorecard_processor.survey': {
            'Meta': {'object_name': 'Survey'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'data_series_groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scorecard_processor.DataSeriesGroup']", 'symmetrical': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'entity_types': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['scorecard_processor.EntityType']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"}),
            'short_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'scorecard_processor.surveytranslation': {
            'Meta': {'unique_together': "(('parent_object', 'lang'),)", 'object_name': 'SurveyTranslation'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        }
    }

    complete_apps = ['scorecard_processor']
