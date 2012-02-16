# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import xlrd
from scorecard_processor import models

class Command(BaseCommand):
    args = '<filename.xls>'
    help = 'Imports a 2012 survey language into the system'
    option_list = BaseCommand.option_list + (
        make_option('--name',
            dest='name',
            help='Give the survey a name'),
        make_option('--lang',
            dest='lang',
            help='Language of the survey'),
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
        lang = options['lang']
        verbose = options['verbose']
        if not name:
            raise CommandError("Require a name for the survey")

        if lang!='fr':
            raise CommandError("'fr' is the only language currently supported")
        
        group = None
        survey= models.Survey.objects.get(name=name, project=models.Project.objects.get())
        questions = dict([(q.identifier,q) for q in survey.question_set.all()])
        qg = survey.questiongroup_set.get(name="Additional questions")
        item,created = qg.questiongrouptranslation_set.get_or_create(lang=lang,defaults={'name':'Des questions supplémentaires'})
        item.name = 'Des questions supplémentaires'
        item.save()

        for q in survey.question_set.filter(question="Voluntary additional information"):
            i,created = q.questiontranslation_set.get_or_create(lang="fr",defaults=dict(question="Informations complémentaires volontaires", help_text="merci d'utiliser cet espace pour plus de détails et le contexte"))
            if not created:
                i.question="Informations complémentaires volontaires"
                i.help_text="merci d'utiliser cet espace pour plus de détails et le contexte"
                i.save()


        skip = True
        sup = None
        order = 0
        sheet = survey_file.sheet_by_name('Survey Tool')
        comment_text = sheet.row(6)[7].value
        for row_num in xrange(7,sheet.nrows):
            row = sheet.row(row_num)

            try:
                q_num = str(int(row[3].value))
                q = row[4].value
            except:
                pass

            question = questions[q_num]
            qt,created  = question.questiontranslation_set.get_or_create(lang=lang, defaults={'question':q})
            qt.question = q
            qt.save()
