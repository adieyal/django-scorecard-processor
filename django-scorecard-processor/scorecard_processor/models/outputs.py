from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from cerial import JSONField

from inputs import Survey
from meta import DataSeries, Project

from scorecard_processor import plugins

class Scorecard(models.Model):
    """Could have multiple transformations grouped for the same 'output', e.g.
    government score card, Country scorecard, 2011 scorecard"""
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project)
    survey = models.ForeignKey(Survey)

    class Meta:
        app_label = "scorecard_processor"

    def __unicode__(self):
        return "Scorecard: %s" % (self.name)

class Indicator(models.Model):
    """Methods are grouped by how they slice data 
    - per ResponseSet
    - per DataSet
    """
    #TODO: validate number of arguments
    #TODO: validate argument positions
    #TODO: operations should be chained? e.g. div(sum(Q1),sum(Q2)) vs. NumDenom(Q1,Q2)
    scorecard = models.ForeignKey(Scorecard)
    operation = models.CharField(max_length=50, choices=plugins.process_plugins_as_choices()) 
    identifier = models.CharField(max_length=25)
    configuration = JSONField(null=True) #For the case of creating check mark outputs

    class Meta:
        app_label = "scorecard_processor"

    def get_values(self, data_series, aggregate_on = None):
        """ Outputs a value from the operation, applying the method to the
        arguments"""
        
    @property
    def method_instance(self):
        if not getattr(self,'_method_instance',None):
            self._method_instance = get_plugin(self.method).plugin(self)
        return self._method_instance

class OperationArgument(models.Model):
    """Arguments need to be ordered and they may be specific question
    responses, or outputs from transitions""" 

    position = models.IntegerField(default=1)
    operation = models.ForeignKey(Indicator)
    instance_content_type = models.ForeignKey(ContentType)
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('sender_content_type', 'sender_id')
    argument_extractor = models.CharField(max_length=30, default='value') #argument / sub-type / how to tease out value. Based on instance type...

    class Meta:
        app_label = "scorecard_processor"
        ordering = ('position',)
        unique_together = ('position','operation')

    def get_values(self, data_series, aggregate_on = None):
        

class ReportRun(models.Model):
    scorecard = models.ForeignKey(Scorecard)
    data_series_source = models.ManyToManyField(DataSeries, blank=True, related_name='report_data_source_set')
    aggregate_on = models.ForeignKey(DataSeries, blank=True, null=True, related_name='report_aggregate_set')
    aggregate_by_entity = models.BooleanField(default=False)

    class Meta:
        app_label = "scorecard_processor"

