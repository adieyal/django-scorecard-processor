from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.generic.base import TemplateView

from models import Entity

reports = {
    'entity':{},
}

def get_entity_urls():
    return patterns('',*[e.get_url() for e in reports['entity'].values()])

class Report(TemplateView):
    @classmethod
    def get_url(cls):
        return url(cls.url, login_required(cls.as_view()), name=cls.__name__+'_report')

class EntityReport(Report):
    """ Report related to an entity """

    def dispatch(self, request, *args, **kwargs):
        self.entity = get_object_or_404(Entity, pk=kwargs['entity_id'])
        return Report.dispatch(self, request, *args, **kwargs)

    def get_data(self):
        raise NotImplementedError

    def get_context_data(self, *args, **kwargs):
        return {'entity':self.entity, 'data':self.get_data()}

    def render_tabular(self):
        """ Renders data in tabular form, using tablib, for multiple output formats """
        raise NotImplementedError

    @classmethod
    def register(cls, name):
        reports['entity'][name] = cls
