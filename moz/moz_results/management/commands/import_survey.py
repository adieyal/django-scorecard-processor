from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import xlrd
from scorecard_processor import models

lookup = {}

class Command(BaseCommand):
    args = '<filename.xls>'
    help = 'Imports a XLS survey into the system'
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
        print(sheet.row(6))
        comment_text = sheet.row(6)[7].value
        section = None
        description = ''
        tick_mode = False
        for row_num in xrange(7,sheet.nrows):
            if row_num in [7,10,11,12,13,21,22] or row_num > 27:
                continue
            row = sheet.row(row_num)
            if row[3].ctype!=0 and int(row[3].value)==17:
                row[0].value = 'Additional questions'
                row[0].ctype = 1

            if row[0].ctype != 0: #Empty
                if section!=None:
                    question = section.question_set.create(survey=survey, identifier=group_name, question="Voluntary additional information", help_text="Please use this space to provide any additional information", widget='textbox')
                section_name = group_name = row[0].value
                if group_name in lookup:
                    section_name = '%s: %s' % (group_name, lookup.get(group_name,group_name))
                section = survey.questiongroup_set.create(name= section_name, help_text=row[1].value)

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
                    '9':'integer',
                    '10':'aid_types',
                }.get(q_num,'multi_currency')

            if q_num == '10':
                if tick_mode == False:
                    tick_mode = True
            else:
                tick_mode = False

            
            if tick_mode and q != row[4].value:
                continue
            else:
                question = models.Question(survey=survey, identifier=q_num, question=q, widget=q_type, group=section)
                if verbose:
                    print('   '+str(question)+'        '+q_type)
                question.save()
        question = section.question_set.create(survey=survey, identifier="General", question="Voluntary additional information", help_text="Please use this space to provide any additional information", widget='textbox')
