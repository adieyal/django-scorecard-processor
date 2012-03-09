from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from collections import defaultdict

from scorecard_processor.plugins.types import Scalar, NOT_APPLICABLE
from scorecard_processor.reports import EntityReport, ProjectReport
from scorecard_processor.models import EntityType, Entity, DataSeries, DataSeriesGroup, Scorecard, Question, ResponseSet
from scorecard_processor.models.outputs import get_responsesets


indicator_5DPa = {"CDC": "0",
"Canada":  "89.78",
"EU":  "100",
"Flanders":  "35.99",
"GFATM": "0",
"Ireland": "100",
"Italy": "33.82",
"Netherlands": "76.63",
"Spain": "65.76",
"Switzerland": "71.16",
"UNFPA": "4.88",
"UNICEF":  "11.3",
"USA": "0",
"UK":  "85.7",
"World Bank":  "0"}


class IndicatorReport(ProjectReport):
    template_name = 'moz_results/indicator_report.html'
    url = r'^indicator/(?P<scorecard_id>\d+)/$'

    @classmethod
    def get_url(cls):
       return url(cls.url, cls.as_view(), name=cls.get_url_name())

    def get_data(self):
        scorecard_id = self.kwargs['scorecard_id']
        scorecard = get_object_or_404(Scorecard, pk=scorecard_id)
        entity_type = [EntityType.objects.get(name='Agency')]
        rs = get_responsesets(scorecard, aggregate_by_entity=True, compare_series=DataSeriesGroup.objects.get(name='Data collection year'), limit_to_entitytype=entity_type)

        operations = OrderedDict()
        for entity, data in rs.items():
            result = scorecard.get_values(data)
            for operation, data in result:
                operations[operation] = operations.get(operation,[])
                if operation.identifier =="5DPa":
                    data[0] = (data[0][0],Scalar(Decimal(indicator_5DPa[entity.name])))
                operations[operation].append((entity,data))
        return operations

    def get_context_data(self,**kwargs):
        context=super(IndicatorReport, self).get_context_data(self,**kwargs)
        indicator = []
        question = Question.objects.get(identifier='10')
        response_sets = ResponseSet.objects.all().select_related('entity').order_by('entity__name')
        for responseset in response_sets:
            r = responseset.get_response(question)
            if r:
                indicator.append((responseset.entity, r.get_value()))
            else:
                indicator.append((responseset.entity, []))
        context['8DP'] = indicator
        return context

    def get_report_links(self, project=None):
        links = []
        name = self.get_url_name()
        project = project or getattr(self,'project')
        for scorecard in project.scorecard_set.all():
            links.append((
                reverse(name,args=[project.pk, scorecard.pk]),
                ': '.join(("Entity report",scorecard.name))
            ))
        return links

IndicatorReport.register('result_by_indicator')
