from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from scorecard_processor.models import Response
from ierg_results.models import Region, Country, Indicator


def graph(request):
    region_id = request.GET.get('region', 0)
    indicator = request.GET.get('indicator', 0)
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target

    if region_id != 'all':
        region_countries = Country.objects.filter(region=region).\
            values_list('name', flat=True)
        values = Response.objects.filter(question__identifier=indicator,
            response_set__entity__name__in=region_countries).\
            values('value', 'response_set__entity__name')
    else:
        values = Response.objects.filter(question__identifier=indicator).\
            values('value', 'response_set__entity__name')

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
                value_item = loads_value.get('Value %i' % i, None)
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
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target

    if region_id != 'all':
        region_countries = Country.objects.filter(region=region).\
            values_list('name', flat=True)
        values = Response.objects.filter(question__identifier=indicator,
            response_set__entity__name__in=region_countries).values('value')
    else:
        values = Response.objects.filter(question__identifier=indicator).\
            values('value')
     
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
                score_item = loads_value.get('Value %i' % i, None)
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
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target

    if region_id != 'all':
        region_countries = Country.objects.filter(region=region).\
            values_list('name', flat=True)
        values = Response.objects.filter(question__identifier=indicator,
            response_set__entity__name__in=region_countries).values('value')
    else:
        values = Response.objects.filter(question__identifier=indicator).\
            values('value')

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
                score_item = loads_value.get('Value %i' % i, None)
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

        region_countries = Country.objects.filter(region=db_region).\
            values_list('name', flat=True)
        values = Response.objects.filter(question__identifier=indicator,
            response_set__entity__name__in=region_countries).\
            values('value', 'response_set__entity__name')

        all_value = []
        max_value = {'country': None, 'value': None}
        min_value = {'country': None, 'value': None}
        for value in values:
            loads_value = simplejson.loads(value['value'])
            current_v = None
            for i in xrange(1, 10):
                current_vi = loads_value.get('Value %i' % i, 0)
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
        l_25 = (len(all_value) - 1) * 0.25
        l_50 = (len(all_value) - 1) * 0.50
        l_75 = (len(all_value) - 1) * 0.75
        if l_25 % 1 == 0:
            region['q1'] = all_value[int(l_25)]
        else:
            region['q1'] = (all_value[int(l_25)] + all_value[int(l_25) + 1]) / 2
        if l_50 % 1 == 0:
            region['q2'] = all_value[int(l_50)]
        else:
            region['q2'] = (all_value[int(l_50)] + all_value[int(l_50) + 1]) / 2
        if l_75 % 1 == 0:
            region['q3'] = all_value[int(l_75)]
        else:
            region['q3'] = (all_value[int(l_75)] + all_value[int(l_75) + 1]) / 2

        region['num_countries'] = values.count()
        regions.append(region)

    values = Response.objects.filter(question__identifier=indicator).\
        values('value')

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
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Indicator, indicator=indicator).target

    if region_id != 'all':
        region_countries = Country.objects.filter(region=region).\
            values_list('name', flat=True)
        values = Response.objects.filter(question__identifier=indicator,
            response_set__entity__name__in=region_countries).\
            values('value', 'response_set__entity__name')
    else:
        values = Response.objects.filter(question__identifier=indicator).\
            values('value', 'response_set__entity__name')

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
                score = loads_value.get('Value %i' % i, None)
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

