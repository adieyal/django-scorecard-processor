from django.db import models
from django.contrib.auth.models import User
from meta import DataSeries, Entity

class Survey(models.Model):
    name = models.CharField(max_length=100)
    data_series = models.ManyToManyField(DataSeries) #Country, Year, Agency

    class Meta:
        app_label = "scorecard_processor"

    def __unicode__(self):
        return "Survey: %s" % (self.name)

class Question(models.Model):
    survey = models.ForeignKey(Survey)
    identifier = models.CharField(max_length=10) #1, 2a, 2b
    question = models.TextField()
    widget = models.CharField(max_length=30, default='text')
    validator = models.CharField(max_length=30, default='anything')

    class Meta:
        app_label = "scorecard_processor"

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

    class Meta:
        app_label = "scorecard_processor"

    def __unicode__(self):
        return "ResponseSet for %s about %s" % (self.survey, self.entity)
    
class Response(models.Model):
    question = models.ForeignKey(Question)
    response_set = models.ForeignKey(ResponseSet)
    value = models.TextField() #Probably should be a cerial field
    baseline = models.TextField(blank=True, null=True) #Probably should be a cerial field
    comment = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    valid = models.BooleanField(default=False) #Has this been validated, and is a valid entry?
    current = models.BooleanField(default=False) #Is this response the current 'active' response for this question

    class Meta:
        app_label = "scorecard_processor"

