from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
from scorecard_processor.models import Response
from ierg_results.models import Region, Country, Indicator
from ierg_results.utils import get_values, calc_values, get_sources,\
                               set_quartiles, get_indicator_value


def graph(request, indicator):
    indicators = [indicator]
    region_id = request.GET.get('region', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    sub_indicators = request.GET.get('sub_indicators')
    if sub_indicators == 'yes':
        indicators.extend(get_object_or_404(Indicator, indicator=indicator).\
            sub_indicators.all().values_list('indicator', flat=True))

    json = []
    for indicator_item in indicators:
        target = get_object_or_404(Indicator, indicator=indicator_item).target
        values = get_values(region_id, region, indicator_item)
        sources = get_sources(values)

        countries = []
        for value in values:
            country = {}
            country['name'] = value['response_set__entity__name']
            loads_value = simplejson.loads(value['value'])
            skeys = [key for key in loads_value.keys() if key.startswith('Source')]
            skeys.sort()
            source = None
            for key in skeys:
                source_key = loads_value.get(key)
                if source_key is not None and source_key != '':
                    source = source_key
            source_id = None
            for sources_item in sources:
                if sources_item['name'] == source:
                    source_id = sources_item['id']
            country['source'] = source_id
            vkeys = [key for key in loads_value.keys() if key.startswith('Value')]
            vkeys.sort()
            score = None
            for key in vkeys:
                score_key = calc_values(loads_value.get(key))
                if score_key is not None and score_key != '':
                    score = score_key
            country['score'] = score
            countries.append(country)

        json_item = {}
        if region_id != 'all':
            json_item['region'] = region.name
        else:
            json_item['region'] = 'All regions'
        json_item['indicator'] = indicator_item
        json_item['target'] = target
        json_item['sources'] = sources
        json_item['countries'] = countries
        json.append(json_item)

    json = simplejson.dumps(json)
    return HttpResponse(json, content_type='application/json')


def aggregate(request, indicator):
    indicators = [indicator]
    region_id = request.GET.get('region', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    sub_indicators = request.GET.get('sub_indicators')
    if sub_indicators == 'yes':
        indicators.extend(get_object_or_404(Indicator, indicator=indicator).\
            sub_indicators.all().values_list('indicator', flat=True))

    json = []
    for indicator_item in indicators:
        values = get_values(region_id, region, indicator_item)
        sources = get_sources(values)

        score_items = []
        for value in values:
            loads_value = simplejson.loads(value['value'])
            vkeys = [key for key in loads_value.keys() if key.startswith('Value')]
            vkeys.sort()
            score_item = None
            for key in vkeys:
                score_key = calc_values(loads_value.get(key))
                if score_key is not None and score_key != '':
                    score_item = score_key
            if score_item is not None:
                score_items.append(score_item)
        score = None
        if len(score_items):
            score = int(round(sum(score_items) / len(score_items)))

        json_item = {}
        if region_id != 'all':
            json_item['region'] = region.name
        else:
            json_item['region'] = 'All regions'
        json_item['indicator'] = indicator_item
        json_item['sources'] = sources
        json_item['score'] = score
        json.append(json_item)

    json = simplejson.dumps(json)
    return HttpResponse(json, content_type='application/json')


def summary(request, indicator):
    indicators = [indicator]
    region_id = request.GET.get('region', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    sub_indicators = request.GET.get('sub_indicators')
    if sub_indicators == 'yes':
        indicators.extend(get_object_or_404(Indicator, indicator=indicator).\
            sub_indicators.all().values_list('indicator', flat=True))

    json = []
    for indicator_item in indicators:
        target = get_object_or_404(Indicator, indicator=indicator_item).target
        values = get_values(region_id, region, indicator_item)
        sources = get_sources(values)

        no_data = 0
        achieved = 0
        not_achieved = 0
        for value in values:
            loads_value = simplejson.loads(value['value'])
            score = loads_value.get('Yes/No')
            if score.lower() == 'yes':
                achieved += 1
            elif score.lower() == 'no':
                not_achieved += 1
            else:
                no_data += 1

        all_score_items = no_data + achieved + not_achieved
        no_data_value = round((float(no_data) / all_score_items) * 100)
        achieved_value = round((float(achieved) / all_score_items) * 100)
        not_achieved_value = round((float(not_achieved) / all_score_items) * 100)

        json_item = {}
        if region_id != 'all':
            json_item['region'] = region.name
        else:
            json_item['region'] = 'All regions'
        json_item['indicator'] = indicator_item
        json_item['sources'] = sources
        json_item['scores'] = {}
        json_item['scores']['no_data'] = {'countries': no_data,
            'value': no_data_value}
        json_item['scores']['achieved_target'] = {'countries': achieved,
            'value': achieved_value}
        json_item['scores']['not_achieved_target'] = {'countries': not_achieved,
            'value': not_achieved_value}
        json_item['target'] = target
        json.append(json_item)

    json = simplejson.dumps(json)
    return HttpResponse(json, content_type='application/json')


def box(request, indicator):
    indicators = [indicator]
    db_regions = Region.objects.all()
    sub_indicators = request.GET.get('sub_indicators')
    if sub_indicators == 'yes':
        indicators.extend(get_object_or_404(Indicator, indicator=indicator).\
            sub_indicators.all().values_list('indicator', flat=True))

    json = []
    for indicator_item in indicators:
        target = get_object_or_404(Indicator, indicator=indicator_item).target

        regions = []
        for db_region in db_regions:
            region = {}
            region['name'] = db_region.name
            values = get_values(None, db_region, indicator_item)

            all_value = []
            max_value = {'country': None, 'value': None}
            min_value = {'country': None, 'value': None}
            for value in values:
                loads_value = simplejson.loads(value['value'])
                vkeys = [key for key in loads_value.keys() if key.startswith('Value')]
                vkeys.sort()
                current_v = None
                for key in vkeys:
                    current_vkey = calc_values(loads_value.get(key))
                    if current_vkey is not None and current_vkey != '':
                        current_v = current_vkey
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

        values = get_values('all', db_region, indicator_item)
        sources = get_sources(values)

        json_item = {}
        json_item['indicator'] = indicator_item
        json_item['target'] = target
        json_item['regions'] = regions
        json_item['sources'] = sources
        json.append(json_item)

    json = simplejson.dumps(json)
    return HttpResponse(json, content_type='application/json')


def achieved(request, indicator):
    indicators = [indicator]
    region_id = request.GET.get('region', 0)
    region = None
    if region_id != 'all':
        region = get_object_or_404(Region, id=region_id)
    sub_indicators = request.GET.get('sub_indicators')
    if sub_indicators == 'yes':
        indicators.extend(get_object_or_404(Indicator, indicator=indicator).\
            sub_indicators.all().values_list('indicator', flat=True))

    json = []
    for indicator_item in indicators:
        target = get_object_or_404(Indicator, indicator=indicator_item).target
        values = get_values(region_id, region, indicator_item)
        sources = get_sources(values)

        countries = []
        for value in values:
            country = {}
            country['name'] = value['response_set__entity__name']
            loads_value = simplejson.loads(value['value'])
            skeys = [key for key in loads_value.keys() if key.startswith('Source')]
            skeys.sort()
            source = None
            for key in skeys:
                source_key = loads_value.get(key)
                if source_key is not None and source_key != '':
                    source = source_key
            source_id = None
            for sources_item in sources:
                if sources_item['name'] == source:
                    source_id = sources_item['id']
            country['source'] = source_id
            vkeys = [key for key in loads_value.keys() if key.startswith('Value')]
            vkeys.sort()
            score = None
            for key in vkeys:
                score_key = calc_values(loads_value.get(key))
                if score_key is not None and score_key != '':
                    score = score_key
            country['score'] = score
            rating_column = loads_value.get('Yes/No')
            if rating_column.lower() == 'yes':
                country['rating'] = 'tick'
            elif rating_column.lower() == 'no':
                country['rating'] = 'cross'
            else:
                country['rating'] = 'missing'
            countries.append(country)

        json_item = {}
        if region_id != 'all':
            json_item['region'] = region.name
        else:
            json_item['region'] = 'All regions'
        json_item['indicator'] = indicator_item
        json_item['target'] = target
        json_item['sources'] = sources
        json_item['countries'] = countries
        json.append(json_item)

    json = simplejson.dumps(json)
    return HttpResponse(json, content_type='application/json')


def scorecard_country(request, country_id):
    country = get_object_or_404(Country, id=country_id)
    indicators_id = [1.1, 1.2, 1.3, 1.7, 2.2, 2.3, 3.1, 3.2, 4.1, 4.3, 5.1, 6.1, 7.1, 8.1]

    indicators = []
    for indicator_id in indicators_id:
        indicator_object = {}
        indicator_object['id'] = indicator_id
        indicator_object['value'] = get_indicator_value(country, indicator_id)
        indicators.append(indicator_object)

    json = {}
    json['country_name'] = country.name
    if country.flag:
        json['country_flag'] = settings.STATIC_URL + 'flags/' + country.flag
    else:
        json['country_flag'] = None
    json['indicators'] = indicators
    json = simplejson.dumps(json)

    return HttpResponse(json, content_type='application/json')

