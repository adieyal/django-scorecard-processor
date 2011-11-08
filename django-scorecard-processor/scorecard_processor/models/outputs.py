from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType
from inputs import Survey
from meta import DataSeries

from scorecard_processor import plugins

class Scorecard(models.Model):
    """Could have multiple transformations grouped for the same 'output', e.g.
    government score card, Country scorecard, 2011 scorecard"""
    name = models.CharField(max_length=50)
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
    scorecard = models.ForeignKey(Scorecard)
    operation = models.CharField(max_length=50, choices=plugins.plugins_as_choices()) 
    identifier = models.CharField()
    limit_data_series = models.ManyToManyField(DataSeries) # none means no filter, adding some in filters outputs

    class Meta:
        app_label = "scorecard_processor"

    def get_values(self, response_set, data_series):
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
    operation = models.ForeignKey(Operation)
    instance_content_type = models.ForeignKey(ContentType)
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('sender_content_type', 'sender_id')
    #argument / sub-type / how to tease out value

    class Meta:
        app_label = "scorecard_processor"
        ordering = ('position',)
        unique_together = ('position','operation')
