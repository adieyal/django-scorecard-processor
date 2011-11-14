from django.db import models
from django.db.models.query import QuerySet
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from cerial import JSONField

from inputs import Survey, ResponseSet
from meta import DataSeriesGroup, Project

from scorecard_processor import plugins

class Scorecard(models.Model):
    """Could have multiple transformations grouped for the same 'output', e.g.
    government score card, Country scorecard, 2011 scorecard"""
    name = models.CharField(max_length=50)
    project = models.ForeignKey(Project)

    class Meta:
        app_label = "scorecard_processor"

    def __unicode__(self):
        return "Scorecard: %s" % (self.name)

    def get_values(self, responsesets, group_by = None):
        result = {}
        #TODO: this is going to break with hierachy
        for indicator in self.operation_set.filter(indicator=True):
            result[indicator.identifier] = indicator.get_values(responsesets)
        return result

class Operation(models.Model):
    """Methods are grouped by how they slice data 
    - per ResponseSet
    - per DataSet
    """
    #TODO: validate number of arguments
    #TODO: validate argument positions
    #TODO: operations should be chained? e.g. div(sum(Q1),sum(Q2)) vs. NumDenom(Q1,Q2)
    #TODO: rework as django-mptt?
    scorecard = models.ForeignKey(Scorecard)
    operation = models.CharField(max_length=50, choices=plugins.process_plugins_as_choices()) 
    identifier = models.CharField(max_length=25)
    configuration = JSONField(null=True, blank=True) #For the case of creating check mark outputs
    indicator = models.BooleanField(default=False, help_text="Is this an output operation, or a pre-cursor to output?")

    class Meta:
        app_label = "scorecard_processor"

    def __init__(self, *args, **kwargs):
        super(Operation,self).__init__(*args, **kwargs)
        self.plugin = plugins.register.get_process_plugin(self.operation).plugin

    def get_values(self, responsesets):
        """ Outputs a value from the operation, applying the method to the
        arguments"""
        return self.plugin(self, responsesets).process()

        
class OperationArgument(models.Model):
    """Arguments need to be ordered and they may be specific question
    responses, or outputs from transitions""" 

    position = models.IntegerField(default=1)
    operation = models.ForeignKey(Operation)
    instance_content_type = models.ForeignKey(ContentType)
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('instance_content_type', 'instance_id')
    argument_extractor = models.CharField(max_length=30, default='value') #argument / sub-type / how to tease out value. Based on instance type...

    class Meta:
        app_label = "scorecard_processor"
        ordering = ('position',)
        unique_together = ('position','operation')

    def get_values(self, responsesets, group_by=None):
        response = self.instance.get_values(responsesets)
        if isinstance(response, QuerySet):
            return [item.get_value() for item in response]
        
class ReportRun(models.Model):
    scorecard = models.ForeignKey(Scorecard)
    source_data = JSONField() #Field which can be resolved to a list or queryset of ResponseSets
    aggregate_on = models.ForeignKey(DataSeriesGroup, blank=True, null=True)
    aggregate_by_entity = models.BooleanField(default=False)

    class Meta:
        app_label = "scorecard_processor"

    def get_responsesets(self):
        source_data = {
            'survey__project__pk':self.scorecard.project.pk, #limit results to the current project
        }
        source_data.update(self.source_data)
        qs = ResponseSet.objects.filter(**source_data).only('id')
        rs_dict = {}
        if self.aggregate_by_entity:
            for entity in self.scorecard.project.entity_set.all():
                e_qs = qs.filter(entity=entity)
                if e_qs.count():
                    rs_dict[entity] = e_qs
        else:
            for dataseries in self.aggregate_on.dataseries_set.all():
                ds_qs = qs.filter(data_series=dataseries)
                if ds_qs.count():
                    rs_dict[dataseries] = ds_qs
        return rs_dict

    def run(self):
        results = {}
        for key, qs in self.get_responsesets().items():
            results[key] = self.scorecard.get_values(qs)
        return results
