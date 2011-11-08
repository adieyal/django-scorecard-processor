# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'DataSeries'
        db.create_table('scorecard_processor_dataseries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('group', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('scorecard_processor', ['DataSeries'])

        # Adding model 'Entity'
        db.create_table('scorecard_processor_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('scorecard_processor', ['Entity'])

        # Adding model 'Survey'
        db.create_table('scorecard_processor_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('scorecard_processor', ['Survey'])

        # Adding M2M table for field data_series on 'Survey'
        db.create_table('scorecard_processor_survey_data_series', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('survey', models.ForeignKey(orm['scorecard_processor.survey'], null=False)),
            ('dataseries', models.ForeignKey(orm['scorecard_processor.dataseries'], null=False))
        ))
        db.create_unique('scorecard_processor_survey_data_series', ['survey_id', 'dataseries_id'])

        # Adding model 'Question'
        db.create_table('scorecard_processor_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('question', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('scorecard_processor', ['Question'])

        # Adding model 'ResponseSet'
        db.create_table('scorecard_processor_responseset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
            ('respondant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('entity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Entity'])),
        ))
        db.send_create_signal('scorecard_processor', ['ResponseSet'])

        # Adding M2M table for field data_series on 'ResponseSet'
        db.create_table('scorecard_processor_responseset_data_series', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('responseset', models.ForeignKey(orm['scorecard_processor.responseset'], null=False)),
            ('dataseries', models.ForeignKey(orm['scorecard_processor.dataseries'], null=False))
        ))
        db.create_unique('scorecard_processor_responseset_data_series', ['responseset_id', 'dataseries_id'])

        # Adding model 'Response'
        db.create_table('scorecard_processor_response', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Question'])),
            ('response_set', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.ResponseSet'])),
            ('value', self.gf('django.db.models.fields.TextField')()),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('scorecard_processor', ['Response'])

        # Adding model 'Scorecard'
        db.create_table('scorecard_processor_scorecard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
        ))
        db.send_create_signal('scorecard_processor', ['Scorecard'])

        # Adding model 'Operation'
        db.create_table('scorecard_processor_operation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scorecard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Scorecard'])),
            ('method', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('scorecard_processor', ['Operation'])

        # Adding M2M table for field limit_data_series on 'Operation'
        db.create_table('scorecard_processor_operation_limit_data_series', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('operation', models.ForeignKey(orm['scorecard_processor.operation'], null=False)),
            ('dataseries', models.ForeignKey(orm['scorecard_processor.dataseries'], null=False))
        ))
        db.create_unique('scorecard_processor_operation_limit_data_series', ['operation_id', 'dataseries_id'])

        # Adding model 'OperationArgument'
        db.create_table('scorecard_processor_operationargument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Operation'])),
            ('instance_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('instance_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal('scorecard_processor', ['OperationArgument'])


    def backwards(self, orm):
        
        # Deleting model 'DataSeries'
        db.delete_table('scorecard_processor_dataseries')

        # Deleting model 'Entity'
        db.delete_table('scorecard_processor_entity')

        # Deleting model 'Survey'
        db.delete_table('scorecard_processor_survey')

        # Removing M2M table for field data_series on 'Survey'
        db.delete_table('scorecard_processor_survey_data_series')

        # Deleting model 'Question'
        db.delete_table('scorecard_processor_question')

        # Deleting model 'ResponseSet'
        db.delete_table('scorecard_processor_responseset')

        # Removing M2M table for field data_series on 'ResponseSet'
        db.delete_table('scorecard_processor_responseset_data_series')

        # Deleting model 'Response'
        db.delete_table('scorecard_processor_response')

        # Deleting model 'Scorecard'
        db.delete_table('scorecard_processor_scorecard')

        # Deleting model 'Operation'
        db.delete_table('scorecard_processor_operation')

        # Removing M2M table for field limit_data_series on 'Operation'
        db.delete_table('scorecard_processor_operation_limit_data_series')

        # Deleting model 'OperationArgument'
        db.delete_table('scorecard_processor_operationargument')


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
            'Meta': {'object_name': 'OperationArgument'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instance_content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'instance_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'operation': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Operation']"}),
            'order': ('django.db.models.fields.IntegerField', [], {})
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
