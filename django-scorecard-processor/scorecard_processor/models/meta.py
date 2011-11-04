from django.db import models

class DataSeries(models.Model):
    name = models.CharField(max_length=100)
    #TODO: split this into a table
    group = models.CharField(max_length=50,choices=(('country','Country'),('month','Month'),('year','Year')))
    class Meta:
        verbose_name_plural = 'Data Series'
        ordering = ('-group','-name')
        app_label = "scorecard_processor"

    def __unicode__(self):
        return "%s: %s" % (self.group, self.name)

class Entity(models.Model):
    """
    An entity / organisation
    """
    name = models.CharField(max_length=100) 

    class Meta:
        app_label = "scorecard_processor"

    def __unicode__(self):
        return "Entity: %s" % (self.name)

