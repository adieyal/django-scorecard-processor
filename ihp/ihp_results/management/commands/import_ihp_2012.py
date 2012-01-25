from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import xlrd
from scorecard_processor import models

class Command(BaseCommand):
    args = '<filename.xls>'
    help = 'Imports a 2012 legacy survey into the system'
    option_list = BaseCommand.option_list + (
        make_option('--name',
            dest='name',
            help='Give the survey a name'),
        make_option('--verbose',
            dest='verbose',
            default=False,
            action='store_true',
            help='verbose_output'),
        )
    output_transaction = True

    def handle(self, *args, **options):
        survey_file = xlrd.open_workbook(args[0])
        name = options['name']
        verbose = options['verbose']
        if not name:
            raise CommandError("Require a name for the survey")
        
        group = None
        survey, created = models.Survey.objects.get_or_create(name=name, project=models.Project.objects.get())
        survey.question_set.all().delete()
        survey.questiongroup_set.all().delete()

        skip = True
        sup = None
        order = 0
        sheet = survey_file.sheet_by_name('Survey Tool')
        comment_text = sheet.row(2)[10].value
        section = None
        description = ''
        tick_mode = False
        for row_num in xrange(3,sheet.nrows):
            row = sheet.row(row_num)
            if row[3].ctype!=0 and int(row[3].value)==17:
                row[0].value = 'General support'
                row[0].ctype = 1

            if row[0].ctype != 0: #Empty
                if section!=None:
                    question = section.question_set.create(survey=survey, identifier=section.name, question="Voluntary additional information", help_text="Please use this space to provide any additional information", widget='textbox')
                section = survey.questiongroup_set.create(name=row[0].value, help_text=row[1].value)

                if verbose:
                    print("\n")
                    print(section.name)
                    print(' '+section.help_text)


            try:
                q_num = str(int(row[3].value))
                q = row[4].value
            except:
                pass

            q_type = {
                    '1':'yes_no_na_choice',
                    '13':'integer',
                    '14':'yes_no_na_choice',
                    '15':'yes_no_na_choice',
                    '16':'aid_types',
                }.get(q_num,'multi_currency')

            if q_num == '16':
                if tick_mode == False:
                    tick_mode = True
            else:
                tick_mode = False

            
            if tick_mode and q != row[4].value:
                continue
            else:
                question = section.question_set.create(survey=survey, identifier=q_num, question=q, widget=q_type)
                if verbose:
                    print('   '+str(question))
        question = section.question_set.create(survey=survey, identifier=section.name, question="Voluntary additional information", help_text="Please use this space to provide any additional information", widget='textbox')
