# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Project'
        db.create_table('scorecard_processor_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('scorecard_processor', ['Project'])

        # Adding M2M table for field user_set on 'Project'
        db.create_table('scorecard_processor_project_user_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['scorecard_processor.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('scorecard_processor_project_user_set', ['project_id', 'user_id'])

        # Adding model 'GlossaryDefinition'
        db.create_table('scorecard_processor_glossarydefinition', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Project'])),
            ('definition', self.gf('django.db.models.fields.TextField')()),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
        ))
        db.send_create_signal('scorecard_processor', ['GlossaryDefinition'])

        # Adding model 'GlossaryTerm'
        db.create_table('scorecard_processor_glossaryterm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('definition', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.GlossaryDefinition'])),
        ))
        db.send_create_signal('scorecard_processor', ['GlossaryTerm'])

        # Adding model 'DataSeriesGroup'
        db.create_table('scorecard_processor_dataseriesgroup', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Project'])),
            ('reverse_ordering', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('scorecard_processor', ['DataSeriesGroup'])

        # Adding model 'DataSeries'
        db.create_table('scorecard_processor_dataseries', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.DataSeriesGroup'])),
            ('visible', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('scorecard_processor', ['DataSeries'])

        # Adding model 'EntityType'
        db.create_table('scorecard_processor_entitytype', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30, primary_key=True)),
            ('plural', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Project'])),
        ))
        db.send_create_signal('scorecard_processor', ['EntityType'])

        # Adding model 'Entity'
        db.create_table('scorecard_processor_entity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('abbreviation', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('entity_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.EntityType'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Project'])),
        ))
        db.send_create_signal('scorecard_processor', ['Entity'])

        # Adding unique constraint on 'Entity', fields ['name', 'project']
        db.create_unique('scorecard_processor_entity', ['name', 'project_id'])

        # Adding M2M table for field user_set on 'Entity'
        db.create_table('scorecard_processor_entity_user_set', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('entity', models.ForeignKey(orm['scorecard_processor.entity'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('scorecard_processor_entity_user_set', ['entity_id', 'user_id'])

        # Adding model 'Survey'
        db.create_table('scorecard_processor_survey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Project'])),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('scorecard_processor', ['Survey'])

        # Adding M2M table for field data_series_groups on 'Survey'
        db.create_table('scorecard_processor_survey_data_series_groups', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('survey', models.ForeignKey(orm['scorecard_processor.survey'], null=False)),
            ('dataseriesgroup', models.ForeignKey(orm['scorecard_processor.dataseriesgroup'], null=False))
        ))
        db.create_unique('scorecard_processor_survey_data_series_groups', ['survey_id', 'dataseriesgroup_id'])

        # Adding M2M table for field entity_types on 'Survey'
        db.create_table('scorecard_processor_survey_entity_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('survey', models.ForeignKey(orm['scorecard_processor.survey'], null=False)),
            ('entitytype', models.ForeignKey(orm['scorecard_processor.entitytype'], null=False))
        ))
        db.create_unique('scorecard_processor_survey_entity_types', ['survey_id', 'entitytype_id'])

        # Adding model 'SurveyTranslation'
        db.create_table('scorecard_processor_surveytranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('scorecard_processor', ['SurveyTranslation'])

        # Adding model 'QuestionGroup'
        db.create_table('scorecard_processor_questiongroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('ordering', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('help_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('scorecard_processor', ['QuestionGroup'])

        # Adding model 'QuestionGroupTranslation'
        db.create_table('scorecard_processor_questiongrouptranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.QuestionGroup'])),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('help_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('scorecard_processor', ['QuestionGroupTranslation'])

        # Adding model 'Question'
        db.create_table('scorecard_processor_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.QuestionGroup'], null=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('help_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('widget', self.gf('django.db.models.fields.CharField')(default='text', max_length=30)),
            ('validator', self.gf('django.db.models.fields.CharField')(default='anything', max_length=30)),
        ))
        db.send_create_signal('scorecard_processor', ['Question'])

        # Adding unique constraint on 'Question', fields ['survey', 'identifier']
        db.create_unique('scorecard_processor_question', ['survey_id', 'identifier'])

        # Adding model 'QuestionTranslation'
        db.create_table('scorecard_processor_questiontranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_object', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Question'])),
            ('lang', self.gf('django.db.models.fields.CharField')(max_length=5, db_index=True)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('help_text', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('scorecard_processor', ['QuestionTranslation'])

        # Adding model 'ImportMap'
        db.create_table('scorecard_processor_importmap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('example_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('scorecard_processor', ['ImportMap'])

        # Adding model 'ImportFieldMap'
        db.create_table('scorecard_processor_importfieldmap', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('importmap', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.ImportMap'])),
            ('cell', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('field', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Question'])),
        ))
        db.send_create_signal('scorecard_processor', ['ImportFieldMap'])

        # Adding model 'ResponseSet'
        db.create_table('scorecard_processor_responseset', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Survey'])),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_update', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_response_id', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
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
            ('respondant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('value', self.gf('django.db.models.TextField')()),
            ('submission_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('valid', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('current', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('scorecard_processor', ['Response'])

        # Adding model 'ResponseOverride'
        db.create_table('scorecard_processor_responseoverride', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Question'])),
            ('value', self.gf('django.db.models.TextField')()),
        ))
        db.send_create_signal('scorecard_processor', ['ResponseOverride'])

        # Adding M2M table for field data_series on 'ResponseOverride'
        db.create_table('scorecard_processor_responseoverride_data_series', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('responseoverride', models.ForeignKey(orm['scorecard_processor.responseoverride'], null=False)),
            ('dataseries', models.ForeignKey(orm['scorecard_processor.dataseries'], null=False))
        ))
        db.create_unique('scorecard_processor_responseoverride_data_series', ['responseoverride_id', 'dataseries_id'])

        # Adding model 'Scorecard'
        db.create_table('scorecard_processor_scorecard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Project'])),
        ))
        db.send_create_signal('scorecard_processor', ['Scorecard'])

        # Adding model 'Operation'
        db.create_table('scorecard_processor_operation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scorecard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Scorecard'])),
            ('operation', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('configuration', self.gf('django.db.models.TextField')(null=True, blank=True)),
            ('indicator', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('scorecard_processor', ['Operation'])

        # Adding model 'OperationArgument'
        db.create_table('scorecard_processor_operationargument', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('position', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('operation', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Operation'])),
            ('instance_content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('instance_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('argument_extractor', self.gf('django.db.models.fields.CharField')(default='value', max_length=30)),
        ))
        db.send_create_signal('scorecard_processor', ['OperationArgument'])

        # Adding unique constraint on 'OperationArgument', fields ['position', 'operation']
        db.create_unique('scorecard_processor_operationargument', ['position', 'operation_id'])

        # Adding model 'ReportRun'
        db.create_table('scorecard_processor_reportrun', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('scorecard', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.Scorecard'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('aggregate_on', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['scorecard_processor.DataSeriesGroup'], null=True, blank=True)),
            ('aggregate_by_entity', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('compare_series', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='indicator_series_set', null=True, to=orm['scorecard_processor.DataSeriesGroup'])),
        ))
        db.send_create_signal('scorecard_processor', ['ReportRun'])

        # Adding M2M table for field limit_to_dataseries on 'ReportRun'
        db.create_table('scorecard_processor_reportrun_limit_to_dataseries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reportrun', models.ForeignKey(orm['scorecard_processor.reportrun'], null=False)),
            ('dataseries', models.ForeignKey(orm['scorecard_processor.dataseries'], null=False))
        ))
        db.create_unique('scorecard_processor_reportrun_limit_to_dataseries', ['reportrun_id', 'dataseries_id'])

        # Adding M2M table for field limit_to_entity on 'ReportRun'
        db.create_table('scorecard_processor_reportrun_limit_to_entity', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reportrun', models.ForeignKey(orm['scorecard_processor.reportrun'], null=False)),
            ('entity', models.ForeignKey(orm['scorecard_processor.entity'], null=False))
        ))
        db.create_unique('scorecard_processor_reportrun_limit_to_entity', ['reportrun_id', 'entity_id'])

        # Adding M2M table for field limit_to_entitytype on 'ReportRun'
        db.create_table('scorecard_processor_reportrun_limit_to_entitytype', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('reportrun', models.ForeignKey(orm['scorecard_processor.reportrun'], null=False)),
            ('entitytype', models.ForeignKey(orm['scorecard_processor.entitytype'], null=False))
        ))
        db.create_unique('scorecard_processor_reportrun_limit_to_entitytype', ['reportrun_id', 'entitytype_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'OperationArgument', fields ['position', 'operation']
        db.delete_unique('scorecard_processor_operationargument', ['position', 'operation_id'])

        # Removing unique constraint on 'Question', fields ['survey', 'identifier']
        db.delete_unique('scorecard_processor_question', ['survey_id', 'identifier'])

        # Removing unique constraint on 'Entity', fields ['name', 'project']
        db.delete_unique('scorecard_processor_entity', ['name', 'project_id'])

        # Deleting model 'Project'
        db.delete_table('scorecard_processor_project')

        # Removing M2M table for field user_set on 'Project'
        db.delete_table('scorecard_processor_project_user_set')

        # Deleting model 'GlossaryDefinition'
        db.delete_table('scorecard_processor_glossarydefinition')

        # Deleting model 'GlossaryTerm'
        db.delete_table('scorecard_processor_glossaryterm')

        # Deleting model 'DataSeriesGroup'
        db.delete_table('scorecard_processor_dataseriesgroup')

        # Deleting model 'DataSeries'
        db.delete_table('scorecard_processor_dataseries')

        # Deleting model 'EntityType'
        db.delete_table('scorecard_processor_entitytype')

        # Deleting model 'Entity'
        db.delete_table('scorecard_processor_entity')

        # Removing M2M table for field user_set on 'Entity'
        db.delete_table('scorecard_processor_entity_user_set')

        # Deleting model 'Survey'
        db.delete_table('scorecard_processor_survey')

        # Removing M2M table for field data_series_groups on 'Survey'
        db.delete_table('scorecard_processor_survey_data_series_groups')

        # Removing M2M table for field entity_types on 'Survey'
        db.delete_table('scorecard_processor_survey_entity_types')

        # Deleting model 'SurveyTranslation'
        db.delete_table('scorecard_processor_surveytranslation')

        # Deleting model 'QuestionGroup'
        db.delete_table('scorecard_processor_questiongroup')

        # Deleting model 'QuestionGroupTranslation'
        db.delete_table('scorecard_processor_questiongrouptranslation')

        # Deleting model 'Question'
        db.delete_table('scorecard_processor_question')

        # Deleting model 'QuestionTranslation'
        db.delete_table('scorecard_processor_questiontranslation')

        # Deleting model 'ImportMap'
        db.delete_table('scorecard_processor_importmap')

        # Deleting model 'ImportFieldMap'
        db.delete_table('scorecard_processor_importfieldmap')

        # Deleting model 'ResponseSet'
        db.delete_table('scorecard_processor_responseset')

        # Removing M2M table for field data_series on 'ResponseSet'
        db.delete_table('scorecard_processor_responseset_data_series')

        # Deleting model 'Response'
        db.delete_table('scorecard_processor_response')

        # Deleting model 'ResponseOverride'
        db.delete_table('scorecard_processor_responseoverride')

        # Removing M2M table for field data_series on 'ResponseOverride'
        db.delete_table('scorecard_processor_responseoverride_data_series')

        # Deleting model 'Scorecard'
        db.delete_table('scorecard_processor_scorecard')

        # Deleting model 'Operation'
        db.delete_table('scorecard_processor_operation')

        # Deleting model 'OperationArgument'
        db.delete_table('scorecard_processor_operationargument')

        # Deleting model 'ReportRun'
        db.delete_table('scorecard_processor_reportrun')

        # Removing M2M table for field limit_to_dataseries on 'ReportRun'
        db.delete_table('scorecard_processor_reportrun_limit_to_dataseries')

        # Removing M2M table for field limit_to_entity on 'ReportRun'
        db.delete_table('scorecard_processor_reportrun_limit_to_entity')

        # Removing M2M table for field limit_to_entitytype on 'ReportRun'
        db.delete_table('scorecard_processor_reportrun_limit_to_entitytype')


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
            'Meta': {'unique_together': "(('name', 'project'),)", 'object_name': 'Entity'},
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
            'Meta': {'object_name': 'QuestionGroupTranslation'},
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'parent_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.QuestionGroup']"})
        },
        'scorecard_processor.questiontranslation': {
            'Meta': {'object_name': 'QuestionTranslation'},
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
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Project']"})
        },
        'scorecard_processor.surveytranslation': {
            'Meta': {'object_name': 'SurveyTranslation'},
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lang': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent_object': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['scorecard_processor.Survey']"})
        }
    }

    complete_apps = ['scorecard_processor']
