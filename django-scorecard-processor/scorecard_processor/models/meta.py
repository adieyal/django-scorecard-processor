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
    name = models.CharField(max_length=30,primary_key=True)
    project = models.ForeignKey(Project)
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
    name = models.CharField(max_length=100) 
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
