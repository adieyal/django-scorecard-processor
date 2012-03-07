from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, ListView, DeleteView, CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import permalink
from django.utils.translation import ugettext_lazy as _


from models import ResponseSet, Survey, Entity, ReportRun, DataSeries, DataSeriesGroup, Scorecard, ResponseOverride
from models.outputs import get_responsesets
from forms import QuestionForm, ResponseSetForm, AddUserForm, UserForm, PasswordResetForm

from guardian.shortcuts import get_perms, assign, remove_perm, get_objects_for_user, get_users_with_perms

def index(request):
    return render_to_response('scorecard_processor/index.html',{},RequestContext(request))

#################################################################
# Managing reporting, surveys etc.
#################################################################

class SurveyResponses(ListView):
    paginate_by = 20
    def get_queryset(self):
        self.survey = get_object_or_404(Survey, pk=self.kwargs['object_id'])
        qs = ResponseSet.objects.filter(survey=self.survey).select_related('entity').order_by('entity__name')
        self.series = self.kwargs.get('series')
        if self.series:
            qs = qs.filter(data_series__name=self.series)
        self.entity = self.kwargs.get('entity')
        if self.entity:
            self.entity = get_object_or_404(Entity, pk=self.entity)
            qs = qs.filter(entity=self.entity)
        self.count = qs.count()
        return qs

    def get_context_data(self, **kwargs):
        context = super(SurveyResponses,self).get_context_data(**kwargs)
        context['survey'] = self.survey
        context['count'] = self.count
        context['series'] = self.series
        context['entity'] = self.entity
        return context

@login_required
def run_report(request, object_id):
    obj = get_object_or_404(ReportRun, pk=object_id)
    result = obj.run()
    return render_to_response(
        'scorecard_processor/reportrun_run.html',
        {'object':obj, 'report':result},
        RequestContext(request)
    )


#################################################################
# Managing users
#################################################################

class UserView(UpdateView):
    model = User
    form_class = UserForm

    def get_context_data(self, **kwargs):
        context = super(UserView,self).get_context_data(**kwargs)
        context['entities'] = get_objects_for_user(self.object, 'change_entity', Entity)
        return context

    @permalink
    def get_success_url(self):
        return ('show_user',(self.object.pk,))
         

#################################################################
# Managing reporting, surveys etc.
#################################################################

@login_required
def create_override(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    override = ResponseOverride(question=question)
    if request.POST:
        form = ResponseOverrideForm(request.POST, instance=override)
        if form.is_valid():
            override=form.save()
            return HttpResponseRedirect()
    else:
        form = ResponseOverrideForm(request.POST, instance=override)
    return render_to_response('scorecard_processor/create_responseoverride.html', {'form':form}, RequestContext(request))


class SurveyOverrides(DetailView):
    model = Survey
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['survey_id'])

    def get_context_data(self, **kwargs):
        context = super(SurveyResponses,self).get_context_data(**kwargs)
        return context


class ResponseOverrideView(DetailView):
    model = ResponseOverride
    def get_object(self):
        return get_object_or_404(self.model, pk=self.kwargs['override_id'])

    def get_context_data(self, **kwargs):
        context = super(ResponseOverride,self).get_context_data(**kwargs)
        return context


class ResponseOverrideDelete(DeleteView):
    model = ResponseOverride

    def get_object(self, queryset=None):
        """ Hook to ensure object is owned by request.user. """
        obj = super(ResponseOverrideDelete, self).get_object()
        #TODO: only allow deleting of overrides owned by the user
        #if not obj.owner == self.request.user:
        #  raise Http404
        return obj

#################################################################
# Entity oriented
#################################################################

@login_required
def entity_list(request):
    entity_list = Entity.objects.all()
    if not request.user.is_staff:
       entity_list = get_objects_for_user(request.user, 'change_entity', entity_list)

    if len(entity_list) == 1:
        return HttpResponseRedirect(entity_list.get().get_absolute_url())

    return render_to_response('scorecard_processor/entity_list.html', {'object_list':entity_list}, RequestContext(request))

@login_required
def entity_detail(request, object_id):
    entity_list = Entity.objects.all()
    if not request.user.is_staff:
       entity_list = get_objects_for_user(request.user, 'change_entity', entity_list)
    try:
        entity = entity_list.get(pk=object_id)
    except Entity.DoesNotExist:
        raise Http404
    user_set = get_users_with_perms(entity)
    return render_to_response('scorecard_processor/entity_detail.html', {'user_set':user_set, 'object':entity}, RequestContext(request))

@login_required
def entity_add_user(request, entity_id):
    entity = get_object_or_404(Entity, pk=entity_id)
    if request.POST:
        form = AddUserForm(request.POST)
        if form.is_valid():
            #Lookup or create user, add to entity
            email = form.cleaned_data['email']
            form.cleaned_data['username'] = email[:30]
            del form.cleaned_data['email']
            user, created = User.objects.get_or_create(email=email, defaults=form.cleaned_data)
            if created:
                reset_form = PasswordResetForm({'email':user.email})
                reset_form.is_valid()
                reset_form.save(email_template_name="registration/new_account.html", subject=_("Account created on %s"))
            assign('change_entity', user, entity)
            return HttpResponseRedirect(reverse('show_user',args=[user.pk]))
    else:
        form = AddUserForm()
    return render_to_response('scorecard_processor/entity/add_user.html', {'object':entity,'form':form}, RequestContext(request))

@login_required
def entity_remove_user(request, entity_id, user_id):
    entity = get_object_or_404(Entity, pk=entity_id)
    user = get_object_or_404(User, pk=user_id)
    remove_perm('change_entity', user, entity)
    return HttpResponseRedirect(entity.get_absolute_url())
        

#################################################################
# User response section
#################################################################

@login_required
def add_survey(request, object_id, survey_id):
    survey = get_object_or_404(Survey, pk=survey_id)
    entity = get_object_or_404(Entity, pk=object_id)
    if not request.user.is_staff and 'change_entity' not in get_perms(request.user, entity):
        raise Http404
    instance = ResponseSet(
                    survey=survey,
                    entity=entity
                )
    form = ResponseSetForm
    if request.POST:
        form = form(request.POST, instance = instance)
        if form.is_valid():
            responseset = form.save()
            return HttpResponseRedirect(responseset.get_absolute_url())
    else:
        form = form(instance = instance)
    return render_to_response('scorecard_processor/respond/add_survey.html',{'survey':survey, 'entity':entity, 'form':form},RequestContext(request))

@login_required
def edit_survey(request, object_id, responseset_id):
    #TODO handle dataset updates/additions/listing
    responseset = get_object_or_404(ResponseSet, pk=responseset_id)
    survey = responseset.survey
    entity = get_object_or_404(Entity, pk=object_id)
    if not request.user.is_staff and 'change_entity' not in get_perms(request.user, entity):
        raise Http404
    form = QuestionForm
    
    if request.POST:
        form = form(request.POST, survey=survey, instance=responseset, user=request.user)
        if form.is_valid():
            form.save()
            next_section = request.POST.get('next')
            if next_section:
                return HttpResponseRedirect('%s#%s' % (responseset.get_absolute_url(), next_section))
            else:
                return HttpResponseRedirect('%s#responseset_%s' % (responseset.entity.get_absolute_url(), responseset.pk))
    else:
        form = form(survey=survey, instance=responseset, user=request.user)

    return render_to_response('scorecard_processor/respond/edit_survey.html',{'responseset':responseset,'entity':entity,'survey':survey, 'form':form},RequestContext(request))

