from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import csv
from scorecard_processor import models

class Command(BaseCommand):
    args = '<filename.csv>'
    help = 'Imports a legacy survey into the system'
    option_list = BaseCommand.option_list + (
        make_option('--name',
            dest='name',
            help='Give the survey a name'),
        )
    output_transaction = True

    def handle(self, *args, **options):
        survey_file = csv.reader(open(args[0],'rb'))
        name = options['name']
        if not name:
            raise CommandError("Require a name for the survey")
        
        group = None
        survey = models.Survey(name=name, project=models.Project.objects.get())
        survey.save()

        skip = True
        sup = None
        order = 0
        last_identifier = ''
        for row in survey_file:
            if not skip: 
                widget = 'text'
                grouper = row[2]
                identifier = row[3]
                question = row[4]
                if grouper:
                    measure = row[1]
                    group_help = row[2]

                    if not group_help:
                        group_help = measure
                    exploded = measure.split(' ')

                    if exploded[0] == 'Number' and exploded[1] == 'of':
                        del exploded[0]
                        del exploded[0]
                        if exploded[0][0].islower():
                            exploded[0] = exploded[0].capitalize()

                    group_name = ' '.join(exploded[0:3])
                    if group_name.endswith(' and'):
                        group_name = group_name[0:-4]
                    if group_name.endswith(' or'):
                        group_name = group_name[0:-3]

                    if sup:
                        print('%s Supplemental: %s' % (last_identifier,sup))
                        group.question_set.create(
                            survey=survey,
                            identifier='%s_sup' % last_identifier,
                            question="Supplemental information",
                            help_text=sup, 
                            widget="textbox"
                        )
                        sup = None

                    print("\n\n%s\n%s" % (group_name,group_help))
                    if not group_name:
                        group_name = group_help
                        group_help = ''
                    group = survey.questiongroup_set.create(
                                name = group_name,
                                ordering = order, 
                                help_text = group_help)
                    order += 1
                try:
                    baseline = row[6]
                except IndexError:
                    baseline = '' 


                try:
                    val = int(baseline.replace(',',''))
                except ValueError:
                    pass
                else:
                    widget = 'integer'
                if 'USD' in question or 'How much' in question:
                    widget = 'fixed_currency'
                if baseline.lower() in ['yes','no']:
                    widget = 'yes_no_na_choice'
                if widget == 'text' and ('number' in question or question.startswith('How many')):
                    widget = 'integer' 
                if widget == 'text' and ('scores' in question and 'scale' in question):
                    widget = 'rating_0_5_half'
                if widget == 'text' and ('date' in question):
                    widget = 'date'

                
                print('%s. %s' % (identifier,question))
                print('%s: %s' % (widget,baseline))
                group.question_set.create(survey=survey, identifier=identifier, question=question, widget=widget)

                try:
                    new_sup = row[11]
                except IndexError:
                    new_sup = None 
                if new_sup:
                    if sup:
                        print('%s Supplemental: %s' % (identifier,sup))
                        group.question_set.create(
                            survey=survey,
                            identifier='%s_sup' % last_identifier,
                            question="Supplemental information", help_text=sup,
                            widget="textbox"
                        )
                    sup = new_sup
                last_identifier = identifier
            if row[0]=='Ind No.':
                skip = False
