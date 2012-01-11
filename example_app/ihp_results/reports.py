from django.shortcuts import get_object_or_404
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from scorecard_processor.reports import EntityReport
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

CountryReport.register('entity_by_country')
