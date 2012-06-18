from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from ierg_results.models import Region, Indicator
from ierg_results.utils import get_values, calc_values, get_sources, set_quartiles


def graph(request):
    region_id = request.GET.get('region', 0)
    indicator = request.GET.get('indicator', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target
    values = get_values(region_id, region, indicator)
    sources = get_sources(values)

    countries = []
    for value in values:
        loads_value = simplejson.loads(value['value'])
        source = None
        value_item = None
        for i in xrange(1, 10):
            source_i = loads_value.get('Source %i' % i, 0)
            if source_i is 0:
                break
            elif source_i is not None:
                source = source_i
                value_item = calc_values(loads_value.get('Value %i' % i, None))
        source_id = None
        for source_item in sources:
            if source_item['name'] == source:
                source_id = source_item['id']
        countries.append({'name': value['response_set__entity__name'],
            'value': value_item, 'source': source_id})

    json = {}
    if region_id != 'all':
        json['region'] = region.name
    else:
        json['region'] = 'All regions'
    json['indicator'] = indicator
    json['target'] = target
    json['sources'] = sources
    json['countries'] = countries
    json = simplejson.dumps(json)

    return HttpResponse(json, content_type='application/json')


def aggregate(request):
    region_id = request.GET.get('region', 0)
    indicator = request.GET.get('indicator', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target
    values = get_values(region_id, region, indicator)
     
    sources = []
    score_items = []
    for value in values:
        loads_value = simplejson.loads(value['value'])
        source = None
        score_item = None
        for i in xrange(1, 10):
            source_i = loads_value.get('Source %i' % i, 0)
            if source_i is 0:
                break
            elif source_i is not None:
                source = source_i
                score_item = calc_values(loads_value.get('Value %i' % i, None))
        if source is not None:
            sources.append(source)
        if score_item is not None:
            score_items.append(score_item)
    sources = list(set(sources))
    for k, v in enumerate(sources):
        sources[k] = {'id': k + 1, 'name': v}
    score = int(round(sum(score_items) / len(score_items)))

    json = {}
    if region_id != 'all':
        json['region'] = region.name
    else:
        json['region'] = 'All regions'
    json['indicator'] = indicator
    json['sources'] = sources
    json['score'] = score
    json = simplejson.dumps(json)

    return HttpResponse(json, content_type='application/json')


def summary(request):
    region_id = request.GET.get('region', 0)
    indicator = request.GET.get('indicator', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target
    values = get_values(region_id, region, indicator)

    sources = []
    no_data = 0
    achieved = 0
    not_achieved = 0
    for value in values:
        loads_value = simplejson.loads(value['value'])
        source = None
        score_item = None
        for i in xrange(1, 10):
            source_i = loads_value.get('Source %i' % i, 0)
            if source_i is 0:
                break
            elif source_i is not None:
                source = source_i
                score_item = calc_values(loads_value.get('Value %i' % i, None))
        if source is not None:
            sources.append(source)
        if score_item is None:
            no_data += 1
        elif score_item >= float(target):
            achieved += 1
        else:
            not_achieved += 1
    sources = list(set(sources))
    for k, v in enumerate(sources):
        sources[k] = {'id': k + 1, 'name': v}

    all_score_items = no_data + achieved + not_achieved
    no_data_value = round((float(no_data) / all_score_items) * 100)
    achieved_value = round((float(achieved) / all_score_items) * 100)
    not_achieved_value = round((float(not_achieved) / all_score_items) * 100)

    json = {}
    if region_id != 'all':
        json['region'] = region.name
    else:
        json['region'] = 'All regions'
    json['indicator'] = indicator
    json['sources'] = sources
    json['scores'] = {}
    json['scores']['no_data'] = {'countries': no_data,
        'value': no_data_value}
    json['scores']['achieved_target'] = {'countries': achieved,
        'value': achieved_value}
    json['scores']['not_achieved_target'] = {'countries': not_achieved,
        'value': not_achieved_value}
    json['target'] = target
    json = simplejson.dumps(json)

    return HttpResponse(json, content_type='application/json')


def box(request):
    indicator = request.GET.get('indicator', 0)
    target = get_object_or_404(Indicator, indicator=indicator).target
    db_regions = Region.objects.all()

    regions = []
    for db_region in db_regions:
        region = {}
        region['name'] = db_region.name
        values = get_values(None, db_region, indicator)

        all_value = []
        max_value = {'country': None, 'value': None}
        min_value = {'country': None, 'value': None}
        for value in values:
            loads_value = simplejson.loads(value['value'])
            current_v = None
            for i in xrange(1, 10):
                current_vi = calc_values(loads_value.get('Value %i' % i, 0))
                if current_vi is 0:
                    break
                elif current_vi is not None:
                    current_v = current_vi
            if current_v is not None:
                all_value.append(current_v)
                if max_value['value'] is None or current_v > max_value['value']:
                    max_value['value'] = current_v
                    max_value['country'] = value['response_set__entity__name']
                if min_value['value'] is None or current_v < min_value['value']:
                    min_value['value'] = current_v
                    min_value['country'] = value['response_set__entity__name']
        region['max_value'] = max_value
        region['min_value'] = min_value

        all_value.sort()
        region = set_quartiles(all_value, region)
        region['num_countries'] = values.count()
        regions.append(region)

    values = get_values('all', db_region, indicator)
    sources = get_sources(values)

    json = {}
    json['indicator'] = indicator
    json['target'] = target
    json['regions'] = regions
    json['sources'] = sources
    json = simplejson.dumps(json)

    return HttpResponse(json, content_type='application/json')


def achieved(request):
    region_id = request.GET.get('region', 0)
    indicator = request.GET.get('indicator', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target
    values = get_values(region_id, region, indicator)
    sources = get_sources(values)

    countries = []
    for value in values:
        country = {}
        loads_value = simplejson.loads(value['value'])
        country['name'] = value['response_set__entity__name']
        source = None
        score = None
        for i in xrange(1, 10):
            source_i = loads_value.get('Source %i' % i, 0)
            if source_i is 0:
                break
            elif source_i is not None:
                source = source_i
                score = calc_values(loads_value.get('Value %i' % i, None))
        country['score'] = score
        if score is None:
            country['rating'] = 'missing'
        elif score >= float(target):
            country['rating'] = 'tick'
        else:
            country['rating'] = 'cross'
        source_id = None
        for source_item in sources:
            if source_item['name'] == source:
                source_id = source_item['id']
        country['source'] = source_id
        countries.append(country)

    json = {}
    if region_id != 'all':
        json['region'] = region.name
    else:
        json['region'] = 'All regions'
    json['indicator'] = indicator
    json['target'] = target
    json['sources'] = sources
    json['countries'] = countries
    json = simplejson.dumps(json)

    return HttpResponse(json, content_type='application/json')

