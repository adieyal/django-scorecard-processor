from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from collections import defaultdict

from scorecard_processor.reports import EntityReport, ProjectReport
from scorecard_processor.models import Entity, DataSeries, DataSeriesGroup, Scorecard
from scorecard_processor.models.outputs import get_responsesets

class CountryReport(EntityReport):
    template_name = 'ihp_results/entity_report.html'
    url = r'^country/(?P<scorecard_id>\d+)/$'

    def get_data(self):
        scorecard_id = self.kwargs['scorecard_id']
        scorecard = get_object_or_404(Scorecard, pk=scorecard_id)
        rs = get_responsesets(scorecard, limit_to_entity=[self.entity], aggregate_by_entity=True, aggregate_on=DataSeriesGroup.objects.get(name='Country'),compare_series=DataSeriesGroup.objects.get(name='Data collection year'))
        operations = OrderedDict()
        for country, data in rs[self.entity].items():
            result = scorecard.get_values(data)
            for operation, data in result:
                operations[operation] = operations.get(operation,[])
                operations[operation].append((country,data))
        return operations

    def get_report_links(self, entity=None):
        links = []
        name = self.get_url_name()
        entity = entity or getattr(self,'entity')
        for scorecard in entity.project.scorecard_set.all():
            links.append((
                reverse(name,args=[entity.pk, scorecard.pk]),
                ': '.join(("Country report",scorecard.name))
            ))
        return links

CountryReport.register('entity_by_country')

class AgencyReport(ProjectReport):
    template_name = 'ihp_results/agency_report.html'
    url = r'^agency/(?P<scorecard_id>\d+)/$'

    def get_data(self):
        scorecard_id = self.kwargs['scorecard_id']
        scorecard = get_object_or_404(Scorecard, pk=scorecard_id)
        rs = get_responsesets(scorecard, aggregate_by_entity=True, compare_series=DataSeriesGroup.objects.get(name='Data collection year'))
        operations = OrderedDict()
        for entity, data in rs.items():
            result = scorecard.get_values(data)
            for operation, data in result:
                operations[operation] = operations.get(operation,[])
                operations[operation].append((entity,data))
        return operations

    def get_report_links(self, project=None):
        links = []
        name = self.get_url_name()
        project = project or getattr(self,'project')
        for scorecard in project.scorecard_set.all():
            links.append((
                reverse(name,args=[project.pk, scorecard.pk]),
                ': '.join(("Agency report",scorecard.name))
            ))
        return links

AgencyReport.register('result_by_entity')
