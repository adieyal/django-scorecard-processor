from django import forms
from django.db.models import Q
from django.template.defaultfilters import slugify
from django.utils.functional import lazy
from bootstrap.forms import *
from models.meta import DataSeries
from models.inputs import ResponseSet, Response, ResponseOverride
from models.outputs import OperationArgument
from plugins import register


class QuestionFieldset(Fieldset):
    def __init__(self, question_group, *fields):
        self.legend_html = question_group and ('<legend>%s</legend>' % question_group.i18n.name) or ''
        self.div_id = question_group and 'qg_'+slugify(question_group.pk);
        if not self.div_id:
            self.div_id = 'general'
        
        if question_group and question_group.help_text:
            self.legend_html += "<p class='legend'>%s</p>" % question_group.i18n.help_text
        self.fields = list(fields)

    def add_field(self, field):
        self.fields.append(field)

    def as_html(self, form):
        return u"<div class='pill-pane' id='%s'><fieldset>%s<div class='fields'>%s</div></fieldset></div>" % (self.div_id, self.legend_html, form.render_fields(self.fields))

class ResponseSetForm(forms.ModelForm):
    class Meta:
        model = ResponseSet
        exclude = ('survey','entity','submission_date','last_update','respondant')

    def _get_responseset(self, survey, data_series):
        qs = self.Meta.model.objects.filter(survey=survey)
        #response = self.Meta.model.objects.get(survey=instance.survey, data_series__exact=self.cleaned_data['data_series'])
        for ds in data_series:
            qs = qs.filter(data_series=ds)
        try:
            response = qs.get()
        except self.Meta.model.DoesNotExist:
            response = None
        return response

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit',True)
        kwargs['commit'] = False
        instance = super(ResponseSetForm, self).save(*args,**kwargs)
        response = self._get_responseset(instance.survey, self.cleaned_data['data_series'])
        if response:
            return response
        if commit:
            instance.save()
            self.save_m2m()
        return instance

class AddUserForm(BootstrapForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    

class ArgumentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ArgumentForm, self).__init__(*args, **kwargs)
        # key should be your sortable-field - in your exaple it's *index*
        self.fields['position'].widget = forms.HiddenInput()
        self.fields['position'].label = ''

    class Meta:
        model = OperationArgument

class QuestionForm(BootstrapForm):
    #TODO: save responses / switch to save even if invalid
    #TODO: take a user object to save with each field update
        
    model = ResponseSet
    def __init__(self, *args, **kwargs):
        self.survey = kwargs.pop('survey')
        self.instance = kwargs.pop('instance')
        self.user = kwargs.pop('user')
        super(QuestionForm, self).__init__(*args, **kwargs)
        general = []
        self.layout = []

        for group in self.survey.questiongroup_set.all().select_related('question'):
            fieldset = QuestionFieldset(group)
            for question in group.question_set.all():
                self.add_field_from_question(question)
                fieldset.add_field('q_%s' % question.pk)
            self.layout.append(fieldset)

        general = self.survey.question_set.filter(group=None)
        if general:
            questions = []
            for question in general:
                self.add_field_from_question(question)
                questions.append('q_%s' % question.pk)
            self.layout.append(Fieldset('',*questions))

        self.initial.update(dict([
                ('q_%s' % response.question.pk, response.get_value()) 
                for response in self.instance.response_set.filter(current=True)
            ]))
            
    def add_field_from_question(self, question):
        field = register.get_input_plugin(question.widget).plugin
        question_tuple = question.i18n
        self.fields['q_%s' % question.pk] = field(
                    label="""<span class="identifier">%s.</span> 
                            <span class="question">%s</span>""" % (question_tuple.identifier, question_tuple.question),
                    help_text=question_tuple.help_text,
                    required=False
        )

    def save(self):
        if not self.instance.pk:
            self.instance.save()
        for question in self.survey.question_set.all():
            value = self.cleaned_data['q_%s' % question.pk]
            # Only create a new 'response' if the existing response is
            # different
            try:
                instance = self.instance.response_set.get(
                    question = question,
                    current = True
                )
            except Response.DoesNotExist:
                instance = None

            if not value and not instance:
                continue

            if instance and instance.get_value() != value:
                instance = None

            if not instance:
                instance = Response(
                    response_set = self.instance,
                    respondant = self.user,
                    question = question,
                    valid = True,
                    current = True
                )
                instance.value = {'value':value}
                instance.save()

class ResponseOverrideForm(BootstrapModelForm):
    class Meta:
        model=ResponseOverride
        exclude = ('question',)

from guardian.shortcuts import get_objects_for_user, assign, remove_perm

def get_form_choices():
    return tuple(((ds.pk, ds.name) for ds in DataSeries.objects.filter(group__name="Country")))

class UserForm(BootstrapForm):
    usable_countries = forms.MultipleChoiceField(required=False, choices=lazy(get_form_choices, tuple)(), widget=forms.CheckboxSelectMultiple, label="Countries the user can <strong>respond to</strong> surveys for")
    read_countries = forms.MultipleChoiceField(required=False, choices=lazy(get_form_choices, tuple)(), widget=forms.CheckboxSelectMultiple, label="Countries the user can <strong>view</strong> responses for" )
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(UserForm, self).__init__(*args, **kwargs)
        self.can_use = get_objects_for_user(self.instance, 'can_use', DataSeries)
        self.can_view = get_objects_for_user(self.instance, 'can_view', DataSeries)
        self.initial['usable_countries']=[i.pk for i in self.can_use]
        self.initial['read_countries']=[i.pk for i in self.can_view]

    def save(self, *args, **kwargs):
        for permission, key in [('can_use','usable_countries'),('can_view','read_countries')]:
            before = set(self.initial[key])
            after = set(self.cleaned_data[key])
            removed = DataSeries.objects.filter(pk__in= before - after)
            added = DataSeries.objects.filter(pk__in=after-before)
            for ds in removed:
                remove_perm(permission, self.instance, ds)
            for ds in added:
                assign(permission, self.instance, ds)
        return self.instance
