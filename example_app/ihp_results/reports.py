from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from scorecard_processor.models import Entity, DataSeries, DataSeriesGroup, Scorecard
from scorecard_processor.models.outputs import get_responsesets


class EntityReport(EntityReport):
    template = 'ihp_results/entity_report.html'
    url_pattern = r'^(?P<scorecard_id>\d+)/$'

    def run_report():
        scorecard_id = self.args['scorecard_id']
        scorecard = get_object_or_404(Scorecard, pk=scorecard_id)
        rs = get_responsesets(scorecard, limit_to_entity=[self.entity], aggregate_by_entity=True, aggregate_on=DataSeriesGroup.objects.get(name='Country'),compare_series=DataSeriesGroup.objects.get(name='Data collection year'))
        operations = OrderedDict()
        for country, data in rs[self.entity].items():
            result = scorecard.get_values(data)
            for operation, data in result:
                operations[operation] = operations.get(operation,[])
                operations[operation].append((country,data))
        return operations
