from django.shortcuts import get_object_or_404
from django.utils import simplejson
from scorecard_processor.models import Response
from ierg_results.models import Country


def get_values(region_id, region, indicator):
    if region_id == 'all':
        values = Response.objects.filter(question__identifier=indicator).\
            values('value', 'response_set__entity__name')
    else:
        region_countries = Country.objects.filter(region=region).\
            values_list('name', flat=True)
        values = Response.objects.filter(question__identifier=indicator,
            response_set__entity__name__in=region_countries).\
            values('value', 'response_set__entity__name')
    return values


def calc_values(value):
    if isinstance(value, basestring):
        if '-' in value:
            values = [float(value) for value in value.split('-')]
            value = sum(values) / len(values)
        elif '<' in value:
            value = float(value.replace('<', '')) / 2
        elif '>' in value:
            value = (float(value.replace('>', '')) + 100) / 2
    return value


def get_sources(values):
    sources = []
    for value in values:
        loads_value = simplejson.loads(value['value'])
        source = None
        for i in xrange(1, 10):
            source_i = loads_value.get('Source %i' % i, 0)
            if source_i is 0:
                break
            elif source_i is not None:
                source = source_i
        if source is not None:
            sources.append(source)
    sources = list(set(sources))
    for k, v in enumerate(sources):
        sources[k] = {'id': k + 1, 'name': v}
    return sources


def set_quartiles(all_value, region):
    l_25 = (len(all_value) - 1) * 0.25
    l_50 = (len(all_value) - 1) * 0.50
    l_75 = (len(all_value) - 1) * 0.75
    if l_25 % 1 == 0:
        region['q1'] = round(all_value[int(l_25)], 2)
    else:
        region['q1'] = round((all_value[int(l_25)] + all_value[int(l_25) + 1]) / 2, 2)
    if l_50 % 1 == 0:
        region['q2'] = round(all_value[int(l_50)], 2)
    else:
         region['q2'] = round((all_value[int(l_50)] + all_value[int(l_50) + 1]) / 2, 2)
    if l_75 % 1 == 0:
        region['q3'] = round(all_value[int(l_75)], 2)
    else:
        region['q3'] = round((all_value[int(l_75)] + all_value[int(l_75) + 1]) / 2, 2)
    return region


def get_indicator_value(country, indicator_id):
    value = get_object_or_404(Response, question__identifier=indicator_id,
        response_set__entity__name=country.name).value
    indicator_value = None
    if indicator_id == 1.1 or indicator_id == 1.2:
        for i in xrange(1, 10):
            indicator_value_i = value.get('Value %i' % i, 0)
            if indicator_value_i is 0:
                break
            elif indicator_value_i is not None:
                indicator_value = indicator_value_i
    elif indicator_id == 8.1:
        indicator_value = value.get('Yes/No Report available 2010 or later')
    else:
        indicator_value = value.get('Yes/No')
    return indicator_value

