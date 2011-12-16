from django.core.management.base import BaseCommand, CommandError
from django.utils import simplejson
from optparse import make_option
import csv
from scorecard_processor import models
import sys
from datetime import datetime, timedelta
import decimal

class Command(BaseCommand):
    args = '<filename.json>'
    help = 'Imports legacy survey data into the system'
    option_list = BaseCommand.option_list + (
        make_option('--flush',
            dest='flush',
            default=False,
            action='store_true',
            help='flush_output'),
        )
    output_transaction = False

    def handle(self, *args, **options):
        now = datetime.now()
        the_future = datetime.now()+timedelta(days=4)
        flush = options['flush']
        reformat = {
            'Yes':'yes',
            'No':'no',
            'N/A':'n/a',
        }
        survey_file = open(args[0],'rb')
        user = models.User.objects.get(pk=1)
        data = simplejson.loads(survey_file.read())
        countries = dict([(country.name, country) for country in models.DataSeriesGroup.objects.get(name="Country").dataseries_set.all()])
        years = dict([(y.name, y) for y in models.DataSeriesGroup.objects.get(name="Year").dataseries_set.all()])
        collections = dict([(c.name, c) for c in models.DataSeriesGroup.objects.get(name="Data collection year").dataseries_set.all()])
        government_survey = models.Survey.objects.get(name="Survey for Government")
        government_survey.questions = dict([(q.identifier, q) for q in government_survey.question_set.all()])
        agency_survey = models.Survey.objects.get(name="Survey for Agencies")
        agency_survey.questions = dict([(q.identifier, q) for q in agency_survey.question_set.all()])
        for agency, response in data.items():
            try:
                a = models.Entity.objects.get(name=agency)
            except models.Entity.DoesNotExist:
                a = None
            if not a:
                try:
                    a = models.Entity.objects.get(abbreviation=agency)
                except models.Entity.DoesNotExist:
                    print("\nNothing for: %s" % agency)
                    a = None
            if a:
                print("\nProcessing: %s" % a)
                for country, questions in response.items():
                    c = countries.get(country)
                    responsesets = {}
                    if 'agency' in questions:
                        survey = agency_survey
                    else:
                        survey = government_survey
                    comment = None
                    sys.stdout.write('  ')
                    for question, value in questions.values()[0].items():
                        if question:
                            comment = comment or value['comment']
                            q = survey.questions.get(question)
                            for collection, response in [('Baseline Collection',value['baseline']), ('2011 Collection',value['latest'])]:
                                year, v = response
                                y = years.get(year,years.get('2007'))
                                col = collections.get(collection,collections.get('2007'))
                                if y and v:
                                    rs = responsesets.get((col,y))
                                    if not rs:
                                        sys.stdout.write('^')
                                        try:
                                            responsesets[(col,y)] = models.ResponseSet.objects.filter(data_series=c).filter(data_series=col).get(
                                                                    survey = survey,
                                                                    entity = a,
                                                                    data_series = y
                                                                    )
                                        except models.ResponseSet.DoesNotExist:
                                            rs = responsesets[(col,y)] = models.ResponseSet(
                                                                    survey = survey,
                                                                    entity = a,
                                                            )
                                            rs.save()
                                            rs.data_series.add(col,c,y)
                                            sys.stdout.write('*')
                                        rs = responsesets[(col,y)]
                                    rs.last_update=the_future #Trick the post_save trigger
                                    #TODO: rather use the plugin to get the right type here
                                    if q.widget == 'yes_no_na_choice':
                                        v = reformat.get(v,v) 

                                    if q.widget.startswith('rating'):
                                        try:
                                            v = decimal.Decimal(v) 
                                        except decimal.InvalidOperation:
                                            sys.stdout.write(':[%s]' % v)
                                            v = None

                                    if q.widget=='fixed_currency':
                                        if len(v.split(',')[-1]) > 2:
                                            v = v.replace(',','')
                                        try:
                                            v = decimal.Decimal(v.replace(' ','')) 
                                        except decimal.InvalidOperation:
                                            sys.stdout.write(':(%s)' % v)
                                            v = None
                                    if v != None:
                                        r = models.Response(
                                            response_set=rs,
                                            respondant=user,
                                            question=q,
                                            valid=True,
                                            current=True,
                                        )

                                        r.value = {'value':v}
                                        r.submission_date = now
                                        r.save()
                                        sys.stdout.write('.')
                                        if flush:
                                            sys.stdout.flush()
                            if comment:
                                q = survey.questions.get('%s_sup' % question)
                                if q:
                                    r = models.Response(
                                        response_set=rs,
                                        respondant=user,
                                        question=q,
                                        valid=True,
                                        current=True,
                                        value='',
                                    )
                                    r.value = {'value':comment}
                                    r.submission_date = now
                                    r.save()
                                    sys.stdout.write('!')
                                    if flush:
                                        sys.stdout.flush()
                                    comment = None
                    print('  %s' % country)
