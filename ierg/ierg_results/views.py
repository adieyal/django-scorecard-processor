from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.utils import simplejson
#from django.core import serializers
from scorecard_processor.models import Response, Entity
from ierg_results.models import Region, Country, Target


def graph(request):
    region_id = request.GET.get('region', 0)
    target_id = request.GET.get('target', 0)
    region = get_object_or_404(Region, id=region_id)
    target = get_object_or_404(Target, id=target_id)
    identifier = target.identifier

    region_countries = Country.objects.filter(region=region).\
        values_list('name', flat=True)
    values = Response.objects.filter(question__identifier=identifier,
        response_set__entity__name__in=region_countries).\
        values('value', 'response_set__entity__name')

    sources = []
    for value in values:
        loads_value = simplejson.loads(value['value'])
        source = None
        for i in xrange(1, len(loads_value)):
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
        for i in xrange(1, len(loads_value)):
            source_i = loads_value.get('Source %i' % i, 0)
            if source_i is 0:
                break
            elif source_i is not None:
                source = source_i
        source_id = 0
        for source_item in sources:
            if source_item['name'] == source:
                source_id = source_item['id']
        countries.append({'name': value['response_set__entity__name'],
            'source': source_id})

    json = {}
    json['region'] = region.name
    json['identifier'] = target.identifier
    json['target'] = target.target
    json['sources'] = sources
    json['countries'] = countries
    json = simplejson.dumps(json)

    #json = serializers.serialize('json', responses)
    #json2 = simplejson.dumps(list(values))
    return HttpResponse(json, content_type='application/json')

