from datetime import datetime, timedelta
import time
from collections import defaultdict

from django.core.cache import cache
from django.db import models
from django.db.models.query import QuerySet, Q
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from cerial import PickleField, JSONField

from inputs import Survey, ResponseSet
from meta import DataSeriesGroup, DataSeries, Project, Entity, EntityType

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

    @models.permalink
    def get_absolute_url(self):
        return ('show_scorecard',(str(self.project.pk),str(self.pk)))

    def get_values(self, responsesets):
        result = []

        if not hasattr(self,'indicators'):
            self.indicators = self.operation_set.filter(indicator=True)

        for indicator in self.indicators:
            results = []
            for ds, rs in responsesets:
                results.append((ds,indicator.get_data(rs)))
            result.append((indicator, results))

        return result

class OperationManager(models.Manager):
    def indicators(self):
        return self.filter(indicator=True)

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
    operation = models.CharField(max_length=50, choices=plugins.process_plugins_as_choices(), help_text="How should this data be processed") 
    identifier = models.CharField(max_length=25, help_text="A short identifier for the operation, e.g. budget_spend, 1G")
    description = models.CharField(max_length=200, help_text="Descriptive name for this indicator e.g. Portion of budget spent(%), Total amount spent ($m)")
    configuration = JSONField(null=True, blank=True) #For the case of creating check mark outputs
    indicator = models.BooleanField(default=False, help_text="Is this an output operation, or a pre-cursor to output?")
    objects = OperationManager()

    class Meta:
        app_label = "scorecard_processor"
        ordering = ('identifier',)

    def __init__(self, *args, **kwargs):
        super(Operation,self).__init__(*args, **kwargs)
        if self.operation:
            self.plugin = plugins.register.get_process_plugin(self.operation).plugin
        else:
            self.plugin = None

    def get_arguments(self):
        if not hasattr(self,'_get_arguments'):
            self._get_arguments = []
            for argument in self.operationargument_set.all():
                #In django 1.4 this can change to prefetch_related('instance')
                argument.instance
                self._get_arguments.append(argument)
        return self._get_arguments

    def __unicode__(self):
        return "%s: %s" % (self.identifier, self.get_operation_display())

    def get_data(self, responsesets, getter=None, setter=None):
        """ Outputs a value from the operation, applying the method to the
        arguments"""
        fetched_rs = [rs for rs in responsesets]
        if fetched_rs:
            key = hash(repr([rs.pk for rs in fetched_rs]))
            latest = fetched_rs[0].last_response_id
            #latest = int(time.mktime(fetched_rs[0].last_update.timetuple()))
        else:
            return None

        instance = self.plugin(self, responsesets)
        if instance.allow_cache:
            try:
                result = result_get(self, data_hash = key, latest_item = latest)
            except NoCachedResult:
                result = instance.process()
                result_set(self, data_hash = key, latest_item = latest, data=result)
        else:
            result = instance.process()
        return result


        
class OperationArgument(models.Model):
    """Arguments need to be ordered and they may be specific question
    responses, or outputs from transitions""" 

    position = models.IntegerField(default=0, db_index=True)
    operation = models.ForeignKey(Operation)
    instance_content_type = models.ForeignKey(ContentType)
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('instance_content_type', 'instance_id')
    argument_extractor = models.CharField(max_length=30, default='value') #argument / sub-type / how to tease out value. Based on instance type...

    class Meta:
        app_label = "scorecard_processor"
        ordering = ('position',)
        unique_together = ('position','operation')

    def __unicode__(self):
        return u"%s: %s" % (self.operation.plugin.argument_list[self.position], self.instance) 

    def get_data(self, responsesets, latest=None):
        response = self.instance.get_data(responsesets)
        if isinstance(response, list):
            response = plugins.Vector(response)
        return response

        
"""

Scorecard from 2010 submissions from South Africa, Nigeria, Somalia
    aggregated by country

Scorecard for 2009 submissions from South Africa, for USAID, WHO
    aggregated by entity

Scorecard for 2009 and 2010 for all countries
    aggregated by entity

"""

class ReportRunError(Exception):
    pass

def flatten_response_queryset(response_sets, survey_cache):
    output = []
    for rs in response_sets:
        rs.survey = survey_cache[rs.survey_id]
        output.append(rs)
    return output

def split_sets(split, response_sets, survey_cache, split_entities = False):
    result = []
    if split:
        for ds in split:
            result.append((ds, flatten_response_queryset(response_sets.filter(data_series=ds), survey_cache)))
    else:
        split = [None]
        result.append((None, flatten_response_queryset(response_sets, survey_cache)))
    if split_entities:
        result_dict = defaultdict(list)
        for ds, qs in result:
            filter_dict = defaultdict(list)
            for rs in flatten_response_queryset(response_sets, survey_cache):
                filter_dict[rs.entity].append(rs)
            for entity, data in filter_dict.items():
                result_dict[entity].append((ds, data))
        result = dict(result_dict)
    return result

def get_responsesets(scorecard, compare_series=None, limit_to_dataseries=[], limit_to_entity=[], limit_to_entitytype=[], aggregate_on=None, aggregate_by_entity=None):
    if not aggregate_by_entity and not aggregate_on:
        raise ReportRunError("No aggregation mode selected")

    surveys = dict([(s.pk, s) for s in scorecard.project.survey_set.all()])

    #TODO: Optimisation for django 1.4, add prefetch_related('data_series') for better performance
    qs = ResponseSet.objects.filter(survey__project__pk=scorecard.project_id).select_related('entity','survey')

    result_sets = None
    
    if limit_to_dataseries and len(limit_to_dataseries):
        qs = qs.filter(data_series__in=limit_to_dataseries)
        if compare_series:
            result_sets = [ds for ds in limit_to_dataseries.filter(group=compare_series)] or None

    if len(limit_to_entity):
        qs = qs.filter(entity__in=limit_to_entity)

    if len(limit_to_entitytype):
        qs = qs.filter(entity__entity_type__in=limit_to_entitytype)

    if not result_sets and compare_series:
        result_sets = [ds for ds in compare_series.dataseries_set.all()]
    
    if aggregate_on:
        rs_dict = defaultdict(lambda: defaultdict(list)) 
        for dataseries in aggregate_on.dataseries_set.all():
            ds_qs = qs.filter(data_series=dataseries)
            if ds_qs.count():
                if aggregate_by_entity:
                    for entity, data in split_sets(result_sets, ds_qs, surveys, split_entities=True).items():
                        rs_dict[entity][dataseries] = data
                else:
                    rs_dict[dataseries] = split_sets(result_sets, ds_qs, surveys)
    else:
        rs_dict = split_sets(result_sets, qs, surveys, split_entities=True)
    """
    returns (aggregate_on):
    {
        <dataseries>:<response_set>,
        ...
    }
    or (aggregate_on_entity):
    {
        <entity>:<response_set>,
        ...
    }
    or (aggregate_on_entity, aggregate_on):
    {
        <dataseries>:{
            <entity>:<response_set>,
            ...
        }
        ...
    }

    Where <response_set> is:
        [(None, [ResponseSet, ...]]
    or (compare_series):
        [(DataSeries, [ResponseSet, ...]), ...]
    """
    return rs_dict

class ReportRun(models.Model):
    scorecard = models.ForeignKey(Scorecard)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    #Need one or both methods of aggregation
    aggregate_on = models.ForeignKey(DataSeriesGroup, blank=True, null=True, help_text="Y axis grouping/aggregation of results")
    aggregate_by_entity = models.BooleanField(default=False, help_text="Group Y axis by the entity that submitted the data")

    compare_series = models.ForeignKey(DataSeriesGroup, blank=True, null=True, related_name="indicator_series_set", help_text="(optional) Group results per indicator by data series in this group")

    #Optional filters for underlying responsesets
    limit_to_dataseries = models.ManyToManyField(DataSeries, blank=True, null=True, help_text="(optional) Limit which responses are used as raw data, based on the data series they belong to") #Optionally limit to dataseries
    limit_to_entity = models.ManyToManyField(Entity, blank=True, null=True, help_text="(optional) Limit which entities are reported on") #Optionally limit to entities
    limit_to_entitytype = models.ManyToManyField(EntityType, blank=True, null=True, help_text="(optional) Limit which types of entities are used for raw data") #Optionally limit to entity types

    class Meta:
        app_label = "scorecard_processor"

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('show_report',(str(self.scorecard.project.pk),str(self.pk)))

    def get_responsesets(self):
        return get_responsesets(
                self.scorecard, 
                compare_series=self.compare_series, 
                limit_to_dataseries=self.limit_to_dataseries.all(),
                limit_to_entity=self.limit_to_entity.all(), 
                limit_to_entitytype=self.limit_to_entitytype.all(), 
                aggregate_on=self.aggregate_on, 
                aggregate_by_entity=self.aggregate_by_entity)

    def run(self):
        results = {}
        for key, qs in self.get_responsesets().items():
            if isinstance(qs, list):
                if len(qs) == 0:
                    results[key] = plugins.Vector([])
                    continue

                results[key] = self.scorecard.get_values(qs)

            if isinstance(qs,dict):
                result = []
                for entity, data in qs.items():
                    result.append((entity, self.scorecard.get_values(data)))
                results[key] = plugins.Vector(result)

        return results

def default_expires(*args, **kwargs):
    return datetime.now() + timedelta(days=5)

class NoCachedResult(Exception):
    pass


try:
    import cPickle as pickle
except ImportError:
    import pickle

def result_get(operation, data_hash, latest_item):
    key = '%s_%s_%s' % (operation.pk, data_hash, latest_item)
    result = cache.get(key, NoCachedResult)
    if result == NoCachedResult:
        raise NoCachedResult
    return result

def result_set(operation, data_hash, latest_item, data):
    cache.set('%s_%s_%s' % (operation.pk, data_hash, latest_item), data, 186400)
