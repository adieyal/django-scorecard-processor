from collections import defaultdict, namedtuple
from ordereddict import OrderedDict

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils.functional import lazy
from django.utils import translation

from bootstrap.forms import BootstrapForm, Fieldset

from meta import DataSeries, DataSeriesGroup, Entity, EntityType, Project
from scorecard_processor import plugins

from cerial import JSONField


class SurveyManager(models.Manager):
    use_for_related_fields = True

    def active(self, *args, **kwargs):
        return self.get_query_set().filter(active=True)

i18nSurveyTuple = namedtuple("i18nSurveyTuple","name description short_description")
class Survey(models.Model):
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    data_series_groups = models.ManyToManyField(DataSeriesGroup) 
    entity_types = models.ManyToManyField(EntityType)

    objects = SurveyManager()

    class Meta:
        app_label = "scorecard_processor"

    @models.permalink
    def get_absolute_url(self):
        return ('show_survey',(str(self.project.pk),str(self.pk)))

    def __unicode__(self):
        return "Survey: %s" % (self.name)

    def get_overrides(self):
        #Get all overrides related to this survey's questions
        #Order overrides by how specific they are (i.e. num of data_series)
        if not hasattr(self, '_overrides'):
            self._overrides = defaultdict(list)
            for override in ResponseOverride.objects.\
                                filter(question__in=self.question_set.all()).\
                                select_related('question').\
                                annotate(ds_count=models.Count('data_series')).\
                                order_by('-ds_count'):
                self._overrides[override.question].append(override)
        return self._overrides

    def get_override(self, question):
        return self.get_overrides().get(question,[])

    def get_questions(self):
        if not hasattr(self,'_questions'):
            self._questions = self.question_set.all()
        return self._questions

    @property
    def i18n(self):
        lang = translation.get_language()
        self._i18n_cache = getattr(self,'_i18n_cache',{})
        obj = self._i18n_cache.get(lang)
        if not obj:
            if lang.startswith('en'):
                obj = self
            else:
                try:
                    obj = self.surveytranslation_set.get(lang=lang)
                except SurveyTranslation.DoesNotExist:
                    obj = self
            self._i18n_cache[lang] = obj
        return i18nSurveyTuple(name=obj.name, description=obj.description, short_description=obj.short_description)
        
class SurveyTranslation(models.Model):
    parent_object = models.ForeignKey(Survey)
    lang = models.CharField(max_length=5, db_index=True)
    name = models.CharField(max_length=100)
    short_description = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "scorecard_processor"
        unique_together = ('parent_object','lang')


i18nQuestionGroupTuple = namedtuple("i18nQuestionGroupTuple","name help_text")
class QuestionGroup(models.Model):
    survey = models.ForeignKey(Survey)
    name = models.CharField(max_length=200)
    ordering = models.IntegerField(default=1)
    help_text = models.TextField(blank=True, null=True)
    class Meta:
        app_label = "scorecard_processor"
        ordering = ('ordering','name')
    def __unicode__(self):
        return "%s" % self.name

    @property
    def i18n(self):
        lang = translation.get_language()
        self._i18n_cache = getattr(self,'_i18n_cache',{})
        obj = self._i18n_cache.get(lang)
        if not obj:
            if lang.startswith('en'):
                obj = self
            else:
                try:
                    obj = self.questiongrouptranslation_set.get(lang=lang)
                except QuestionGroupTranslation.DoesNotExist:
                    obj = self
            self._i18n_cache[lang] = obj
        return i18nQuestionGroupTuple(name=obj.name, help_text=obj.help_text)


class QuestionGroupTranslation(models.Model):
    parent_object = models.ForeignKey(QuestionGroup)
    lang = models.CharField(max_length=5, db_index=True)
    name = models.CharField(max_length=200)
    help_text = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "scorecard_processor"
        unique_together = ('parent_object','lang')


i18nQuestionTuple = namedtuple("i18nQuestionTuple","identifier question help_text")
class Question(models.Model):
    survey = models.ForeignKey(Survey)
    group = models.ForeignKey(QuestionGroup, null=True, blank=True)
    identifier = models.CharField(max_length=10) #1, 2a, 2b
    question = models.TextField()
    help_text = models.TextField(blank=True, null=True)
    widget = models.CharField(max_length=30, default='text', choices=lazy(plugins.input_plugins_as_choices,list)())
    validator = models.CharField(max_length=30, default='anything')

    class Meta:
        app_label = "scorecard_processor"
        unique_together = ('survey','identifier')
        ordering = ('group__ordering','id',)

    @property
    def i18n(self):
        lang = translation.get_language()
        self._i18n_cache = getattr(self,'_i18n_cache',{})
        obj = self._i18n_cache.get(lang)
        if not obj:
            if lang.startswith('en'):
                obj = self
            else:
                try:
                    obj = self.questiontranslation_set.get(lang=lang)
                except QuestionTranslation.DoesNotExist:
                    obj = self
            self._i18n_cache[lang] = obj
        return i18nQuestionTuple(identifier=self.identifier, question=obj.question, help_text=obj.help_text)

    def get_widget(self):
        form = BootstrapForm()
        form.fields[self.identifier] = plugins.get_input_plugin(self.widget).plugin(
            label="""<span class="identifier">%s.</span> 
            <span class="question">%s</span>""" % (self.identifier,self.question),
            help_text=self.help_text,
            required=False
        )
        form.layout = [Fieldset('',self.identifier)]
        return form

    def get_overrides(self):
        return self.survey.get_override(self)

    @models.permalink
    def get_absolute_url(self):
      return ('show_survey_question',(str(self.survey.project.pk),str(self.survey.pk),str(self.pk)))

    def get_data(self, responsesets):
        return filter(lambda x: x!=None, [rs.get_response(self) for rs in responsesets])

    def __unicode__(self):
        return "Question: %s. %s" % (self.identifier, self.question)

class QuestionTranslation(models.Model):
    parent_object = models.ForeignKey(Question)
    lang = models.CharField(max_length=5, db_index=True)
    question = models.TextField()
    help_text = models.TextField(blank=True, null=True)

    class Meta:
        app_label = "scorecard_processor"
        unique_together = ('parent_object','lang')


class ImportMap(models.Model):
    survey = models.ForeignKey(Survey)
    name = models.CharField(max_length=200)
    example_file = models.FileField(blank=True, null=True, upload_to="import_example")
    class Meta:
        app_label = "scorecard_processor"


class ImportFieldMap(models.Model):
    importmap = models.ForeignKey(ImportMap)
    cell = models.CharField(max_length=20)
    field = models.ForeignKey(Question)
    class Meta:
        app_label = "scorecard_processor"


#TODO: enforce requirement of members of survey.data_series_groups
class ResponseSet(models.Model):
    """ Survey::ResponseSet, Question::Response """
    survey = models.ForeignKey(Survey)
    submission_date = models.DateTimeField(auto_now_add = True)
    last_update = models.DateTimeField(auto_now_add = True)
    last_response_id = models.PositiveIntegerField(blank=True, null=True)
    entity = models.ForeignKey(Entity)
    editable = models.BooleanField(default=True)
    data_series = models.ManyToManyField(DataSeries) #Country, Year, Agency

    class Meta:
        app_label = "scorecard_processor"
        ordering = ('-last_update',)

    @models.permalink
    def get_absolute_url(self):
        return ('survey_response_edit',(str(self.entity.pk),str(self.pk)))

    def __unicode__(self):
        return "ResponseSet for %s about %s" % (self.survey, self.entity)

    def get_data_series(self):
        if not hasattr(self, '_data_series'):
            self._data_series = self.data_series.all().select_related('group')
        return self._data_series

    def get_data_series_by_type(self):
        return dict([
            (ds.group.name, ds) for ds in self.get_data_series()
        ])

    def set_meta(name, value):
        self._meta = getattr(self,'_meta',{})
        meta, created = self.responsesetmetadata_set.get_or_create(key=name)
        self._meta[name] = meta.value = value
        meta.save()

    def get_meta(name, default=None):
        self._meta = getattr(self,'_meta',{})
        if name not in self._meta:
            try:
                self._meta[key] = self.responsesetmetadata_set.get(key=name).value
            except ResponseSetMetaData.DoesNotExist:
                self._meta[key] = None
        return self._meta[key]

    def get_responses(self):
        if not hasattr(self,'_responses'):
            #Cache responses for this responseset, order by question ordering
            #Overlay responses with relevant responseoverride
            self._responses = OrderedDict()
            responses = dict([(r.question, r) for r in self.response_set.filter(current=True).select_related('question')])
            for question in self.survey.get_questions():
                response = responses.get(question)
                if response:
                    #Ensure the fetched object caches the same responseset object
                    response.response_set = self
                for override in self.survey.get_override(question):
                    if set(override.get_data_series()).issubset(set(self.get_data_series())):
                        override.response = response
                        self._responses[question] = override
                        continue
                self._responses[question] = response
        return self._responses

    def get_response(self, question):
        return self.get_responses().get(question)

class ResponseSetMetaData(models.Model):
    response_set = models.ForeignKey(ResponseSet)
    key = models.CharField(max_length=20, db_index=True)
    value = JSONField() 
    class Meta:
        app_label = "scorecard_processor"
        unique_together = ('response_set','key'),
    

class Response(models.Model):
    question = models.ForeignKey(Question)
    response_set = models.ForeignKey(ResponseSet)
    respondant = models.ForeignKey(User)

    value = JSONField() 
    submission_date = models.DateTimeField(auto_now_add=True)

    valid = models.BooleanField(default=False) #Has this been validated, and is a valid entry?
    current = models.BooleanField(default=True) #Is this response the current 'active' response for this question

    class Meta:
        app_label = "scorecard_processor"

    def get_value(self):
        #TODO: should read something like question.get_validator()(self.value).get_value()
        #This method should output the value cast to the kind of value this field is
        return self.value.get('value')


class ResponseOverride(models.Model):
    question = models.ForeignKey(Question)
    data_series = models.ManyToManyField(DataSeries) #Country, Year, Agency
    value = JSONField() 

    class Meta:
        app_label = "scorecard_processor"

    def get_data_series(self):
        if not hasattr(self, '_data_series'):
            self._data_series = self.data_series.all()
        return self._data_series

    def get_value(self):
        #TODO: should read something like question.get_validator()(self.value).get_value()
        #This method should output the value cast to the kind of value this field is
        return self.value.get('value')

    def set_response(self, response):
        self._response = response

    def get_response(self, response):
        return self._response

    response = property(get_response, set_response)


def invalidate_old_responses(sender, instance, **kwargs):
    if instance.current:
        instance.response_set.response_set.filter(question=instance.question, current=True).exclude(pk=instance.pk).update(current=False)
        if instance.submission_date > instance.response_set.last_update:
            instance.response_set.last_update = instance.submission_date
            instance.response_set.last_response_id = instance.pk
            instance.response_set.save()

post_save.connect(invalidate_old_responses, sender=Response, dispatch_uid="scorecard_processor.invalidate_responses")
