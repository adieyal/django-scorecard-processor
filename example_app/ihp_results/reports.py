from decimal import Decimal
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from collections import defaultdict

from scorecard_processor.plugins.types import Scalar, NOT_APPLICABLE
from scorecard_processor.reports import EntityReport, ProjectReport
from scorecard_processor.models import EntityType, Entity, DataSeries, DataSeriesGroup, Scorecard
from scorecard_processor.models.outputs import get_responsesets

from target_criteria import indicators, criteria_funcs, MissingValueException, CannotCalculateException


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

class Rating(object):
    TICK = 'tick'
    ARROW = 'arrow'
    CROSS = 'cross'
    QUESTION = 'question' 
    NONE = 'none'

class AgencyReport(ProjectReport):
    template_name = 'ihp_results/agency_report.html'
    url = r'^agency/(?P<scorecard_id>\d+)/$'

    def get_rating(self, indicator, base_val, cur_val):

        indicator_data = indicators[indicator.identifier]
        tick_func = criteria_funcs[indicator_data['tick_function']]
        arrow_func = criteria_funcs[indicator_data['arrow_function']]

        if cur_val not in [None, NOT_APPLICABLE]:
            if indicator.identifier in ["5DPa", "5DPb"]:
                if cur_val <= 20:
                    return Rating.TICK
            elif indicator.identifier in ["2DPa"]:
                if cur_val <= 15:
                    return Rating.TICK
            elif indicator.identifier in ["5DPc"]:
                if cur_val == 0:
                    return Rating.TICK
            elif indicator.identifier in ["5Ga"]:
                if base_val not in [None, NOT_APPLICABLE]:
                    if cur_val - base_val >= 0.5:
                        return Rating.TICK
            elif indicator.identifier in ["4G"]:
                if cur_val <= 20:
                    return Rating.TICK

        try:
            if tick_func(float(base_val), float(cur_val), indicator_data['tick_value']):
                return Rating.TICK
            elif arrow_func(float(base_val), float(cur_val), indicator_data['arrow_value']):
                return Rating.ARROW
            else:
                return Rating.CROSS
        except MissingValueException:
            return Rating.QUESTION
        except CannotCalculateException:
            return Rating.NONE


    def get_data(self):
        scorecard_id = self.kwargs['scorecard_id']
        scorecard = get_object_or_404(Scorecard, pk=scorecard_id)
        if scorecard.name.startswith('Agency'):
            entity_type = [EntityType.objects.get(name='agency')]
        else:
            entity_type = [EntityType.objects.get(name='government')]
        rs = get_responsesets(scorecard, aggregate_by_entity=True, compare_series=DataSeriesGroup.objects.get(name='Data collection year'), limit_to_entitytype=entity_type)

        operations = OrderedDict()
        for entity, data in rs.items():
            result = scorecard.get_values(data)
            for operation, data in result:
                operations[operation] = operations.get(operation,[])

                base, curr = data
                base, curr = base[1], curr[1]

                change = ''
                if base is not None and curr is not None:
                    if isinstance(curr, Scalar) and isinstance(curr.get_value(), Decimal):
                        change = Scalar(100)
                        if isinstance(base, Scalar) and isinstance(base.get_value(),Decimal):
                            if base.get_value() == 0:
                                change = ''
                            else:
                                change = Scalar(((curr.get_value() / base.get_value() * 100)-100).quantize(Decimal('1.0')))

                data.append(('% change', change))

                rating = 'none'
                if curr is not None and isinstance(curr,Scalar) and isinstance(curr.get_value(), Decimal):
                    if base != None:
                        rating = self.get_rating(operation, base.get_value(), curr.get_value())
                    else:
                        rating = Rating.NONE

                data.append(('rating', rating))
                #if first:
                #    if len(data)==2:
                #        data.append(('rating',''))
                operations[operation].append((entity,data))
        return operations

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

AgencyReport.register('result_by_entity')
