from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class DataSeries(models.Model):
    name = models.CharField(max_length=100)
    group = models.CharField(max_length=50,choices=(('Country','country'),('Year','year')))
    class Meta:
        verbose_name_plural = 'Data Series'

    def __unicode__(self):
        return "%s: %s" % (self.group, self.name)

class Entity(models.Model):
    """
    An entity / organisation
    """
    name = models.CharField(max_length=100) 

    def __unicode__(self):
        return "Entity: %s" % (self.name)


class Survey(models.Model):
    name = models.CharField(max_length=100)
    data_series = models.ManyToManyField(DataSeries) #Country, Year, Agency
    def __unicode__(self):
        return "Survey: %s" % (self.name)

class Question(models.Model):
    survey = models.ForeignKey(Survey)
    identifier = models.CharField(max_length=10) #1, 2a, 2b
    question = models.TextField()

    def get_value(self, data_series=[], responseset_set=[]):
        return ''

    def __unicode__(self):
        return "Question: %s. %s" % (self.identifier, self.question)

class ResponseSet(models.Model):
    """ Survey::ResponseSet, Question::Response """
    survey = models.ForeignKey(Survey)
    respondant = models.ForeignKey(User)
    submission_date = models.DateTimeField(auto_now_add=True)
    entity = models.ForeignKey(Entity)
    data_series = models.ManyToManyField(DataSeries) #Country, Year, Agency

    def __unicode__(self):
        return "ResponseSet for %s about %s" % (self.survey, self.entity)
    
class Response(models.Model):
    question = models.ForeignKey(Question)
    response_set = models.ForeignKey(ResponseSet)
    value = models.TextField() #Probably should be a cerial field
    comment = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    valid = models.BooleanField(default=False) #Has this been validated, and is a valid entry?
    current = models.BooleanField(default=False) #Is this response the current 'active' response for this question


class Scorecard(models.Model):
    """Could have multiple transformations grouped for the same 'output', e.g.
    government score card, Country scorecard, 2011 scorecard"""
    name = models.CharField(max_length=50)
    survey = models.ForeignKey(Survey)
    def __unicode__(self):
        return "Scorecard: %s" % (self.name)

class Operation(models.Model):
    """Methods are grouped by how they slice data 
    - per ResponseSet
    - per DataSet
    """
    scorecard = models.ForeignKey(Scorecard)
    method = models.CharField(max_length=50) 
    limit_data_series = models.ManyToManyField(DataSeries) # none means no filter, adding some in filters outputs

    def get_values(self, response_set, data_series):
        """ Outputs a value from the operation, applying the method to the
        arguments"""
        return ''

class OperationArgument(models.Model):
    """Arguments need to be ordered and they may be specific question
    responses, or outputs from transitions""" 

    order = models.IntegerField()
    operation = models.ForeignKey(Operation)
    instance_content_type = models.ForeignKey(ContentType)
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('sender_content_type', 'sender_id')

# transition('add_values', Question(1), DataSeries(2011), DataSeries(South Africa)).get_values()
