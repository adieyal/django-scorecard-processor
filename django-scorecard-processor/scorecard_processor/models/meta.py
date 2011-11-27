from django.db import models

class Project(models.Model):
    name = models.CharField(max_length=100) 
    class Meta:
        app_label = "scorecard_processor"

    @models.permalink
    def get_absolute_url(self):
        return ('show_project',[str(self.pk)])

    def __unicode__(self):
        return "Project: %s" % (self.name)

class DataSeriesGroup(models.Model):
    """
    QUESTION - what is the rationale behind this model? Is it simply to add a label to a responseset so that you can retrieve related questionnaires e.g. "Get all the surveys from 2009"?
    """
    name = models.CharField(max_length=30,primary_key=True)
    project = models.ForeignKey(Project)
    "QUESTION - this seems like a strange field to store? Why doesn't the user simply specify the data series in the correct order? "
    reverse_ordering = models.BooleanField(default=False)

    class Meta:
        ordering = ('name',)
        app_label = "scorecard_processor"

    def get_dataseries(self):
        qs = self.dataseries_set.all()
        if self.reverse_ordering:
            qs = qs.order_by('-name')
        return qs


    def __unicode__(self):
        return self.name

class DataSeries(models.Model):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(DataSeriesGroup)

    class Meta:
        verbose_name_plural = 'Data Series'
        ordering = ('-group','name')
        app_label = "scorecard_processor"

    @property
    def data_type(self):
        return self.group.pk

    def __unicode__(self):
        return "%s: %s" % (self.group.pk, self.name)

class EntityType(models.Model):
    name = models.CharField(max_length=30,primary_key=True)
    plural = models.CharField(max_length=30)
    project = models.ForeignKey(Project)
    class Meta:
        app_label = "scorecard_processor"
    def __unicode__(self):
        return "%s / %s" % (self.name, self.plural)

class Entity(models.Model):
    """
    An entity / organisation
    """

    """
    QUESTION - what is the purpose of an entity? Is it a type of organisation that may complete a questionnaire? or does it simply define the set of surveys that need to be completed by a particular entity type?
    """
    name = models.CharField(max_length=100) 

    """
    QUESTION - how does this field get used?
    """
    abbreviation = models.CharField(max_length=30, blank=True, null=True)
    entity_type = models.ForeignKey(EntityType)
    project = models.ForeignKey(Project)

    class Meta:
        app_label = "scorecard_processor"
        unique_together = (('name','project'),)

    @property
    def data_type(self):
        return self.entity_type.pk

    @models.permalink
    def get_absolute_url(self):
        return ('show_entity',(str(self.pk),))

    def __unicode__(self):
        if self.abbreviation:
            return "%s: %s (%s)" % (self.entity_type.pk.capitalize(), self.name, self.abbreviation)
        return "%s: %s" % (self.entity_type.pk.capitalize(), self.name)
