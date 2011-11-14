from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from meta import DataSeries, DataSeriesGroup, Entity, Project

from cerial import JSONField

class Survey(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    data_series_groups = models.ManyToManyField(DataSeriesGroup) 

    class Meta:
        app_label = "scorecard_processor"

    @models.permalink
    def get_absolute_url(self):
      return ('show_survey',(str(self.project.pk),str(self.pk)))

    def __unicode__(self):
        return "Survey: %s" % (self.name)

class Question(models.Model):
    survey = models.ForeignKey(Survey)
    identifier = models.CharField(max_length=10) #1, 2a, 2b
    question = models.TextField()
    help_text = models.TextField(blank=True, null=True)
    widget = models.CharField(max_length=30, default='text')
    validator = models.CharField(max_length=30, default='anything')

    class Meta:
        app_label = "scorecard_processor"
        unique_together = ('survey','identifier')

    @models.permalink
    def get_absolute_url(self):
      return ('show_survey_question',(str(self.survey.project.pk),str(self.survey.pk),str(self.pk)))

    def get_values(self, responsesets):
        return self.response_set.filter(response_set__in=responsesets, current=True)

    def __unicode__(self):
        return "Question: %s. %s" % (self.identifier, self.question)

#TODO: enforce requirement of members of survey.data_series_groups
class ResponseSet(models.Model):
    """ Survey::ResponseSet, Question::Response """
    survey = models.ForeignKey(Survey)
    respondant = models.ForeignKey(User)
    submission_date = models.DateTimeField(auto_now_add = True)
    last_update = models.DateTimeField(auto_now_add = True)
    entity = models.ForeignKey(Entity)
    data_series = models.ManyToManyField(DataSeries) #Country, Year, Agency

    class Meta:
        app_label = "scorecard_processor"
        ordering = ('-last_update',)

    @models.permalink
    def get_absolute_url(self):
      return ('survey_response_edit',(str(self.entity.pk),str(self.pk)))

    def __unicode__(self):
        return "ResponseSet for %s about %s" % (self.survey, self.entity)
    
class Response(models.Model):
    question = models.ForeignKey(Question)
    response_set = models.ForeignKey(ResponseSet)
    value = JSONField() 
    comment = models.TextField(blank=True, null=True) #Possibly move this out?
    submission_date = models.DateTimeField(auto_now_add=True)

    valid = models.BooleanField(default=False) #Has this been validated, and is a valid entry?
    current = models.BooleanField(default=True) #Is this response the current 'active' response for this question

    class Meta:
        app_label = "scorecard_processor"

    def get_value(self):
        return self.value

def invalidate_old_responses(sender, instance, **kwargs):
    if instance.current:
        instance.response_set.response_set.exclude(pk=instance.pk).filter(question=instance.question).update(current=False)
        if instance.submission_date > instance.response_set.last_update:
            instance.response_set.last_update = instance.submission_date
            instance.response_set.save()

post_save.connect(invalidate_old_responses, sender=Response, dispatch_uid="scorecard_processor.invalidate_responses")
