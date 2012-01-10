from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

class Report(object):
    def __init__(self, request, **kwargs):
        self.request = request
        self.args = kwargs

class EntityReport(Report):
    """ Report related to an entity """
    def __init__(self, request, **kwargs):
        Report.__init__(self, request, **kwargs)
        self.entity = get_object_or_404(Entity, kwargs['entity_id'])

    def get_data(self):
        raise NotImplementedError

    def render_response(self):
        return render_to_response(self.template, {'entity':self.entity, 'data':self.get_data()}, RequestContext(self.request))

    def render_tabular(self):
        """ Renders data in tabular form, using tablib, for multiple output formats """
        raise NotImplementedError
