from django.core.management.base import BaseCommand, CommandError
from django.utils import simplejson
from optparse import make_option
import csv
from scorecard_processor import models
import sys

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
    output_transaction = True

    def handle(self, *args, **options):
        flush = options['flush']
        survey_file = open(args[0],'rb')
        user = models.User.objects.get(pk=1)
        data = simplejson.loads(survey_file.read())
        countries = dict([(country.name, country) for country in models.DataSeriesGroup.objects.get(name="Country").dataseries_set.all()])
        years = dict([(y.name, y) for y in models.DataSeriesGroup.objects.get(name="Year").dataseries_set.all()])
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
                            for response in [value['baseline'], value['latest']]:
                                year, v = response
                                y = years.get(year,years.get('2007'))
                                if y and v:
                                    rs = responsesets.get(y)
                                    if not rs:
                                        sys.stdout.write('^')
                                        try:
                                            responsesets[y] = models.ResponseSet.objects.filter(data_series=c).get(
                                                                    respondant = user,
                                                                    survey = survey,
                                                                    entity = a,
                                                                    data_series = y
                                                                    )
                                        except models.ResponseSet.DoesNotExist:
                                            rs = responsesets[y] = models.ResponseSet(
                                                                    respondant = user,
                                                                    survey = survey,
                                                                    entity = a,
                                                            )
                                            rs.save()
                                            rs.data_series.add(c,y)
                                            sys.stdout.write('*')
                                        rs = responsesets[y]
                                    r = models.Response(
                                        response_set=rs,
                                        question=q,
                                        valid=True,
                                        current=True,
                                        value=''
                                    )
                                    r.value = v
                                    r.save()
                                    sys.stdout.write('.')
                                    if flush:
                                        sys.stdout.flush()
                            if comment:
                                q = survey.questions.get('%s_sup' % question)
                                if q:
                                    r = models.Response(
                                        response_set=rs,
                                        question=q,
                                        valid=True,
                                        current=True,
                                        value=''
                                    )
                                    r.value = comment
                                    #r.save()
                                    sys.stdout.write('!')
                                    if flush:
                                        sys.stdout.flush()
                                    comment = None
                                    
                    print('  %s' % country)
