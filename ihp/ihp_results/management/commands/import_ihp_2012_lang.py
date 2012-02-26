# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
import xlrd
from scorecard_processor import models

group_text = {
"1G":  "Accord IHP+ ou entente mutuelle équivalente en place.",
"2Ga": "Plans et stratégie nationaux sectoriels de santé mis en place avec des objectifs et des budgets actuels qui ont été évalués conjointement.",
"2Gb": "Un Plan relatif aux HRH chiffré et fondé sur des preuves est en place et intégré au plan de santé national.",
"3G":  "Proportion de financement public alloué à la santé.",
"4G":  "Part de financement du secteur de la santé qui a été décaissée, par rapport au budget annuel approuvé.",
"5G":  "Les systèmes d’approvisionnement des pays et de gestion des finances publiques (dans le secteur de la santé) a) adhèrent à des pratiques exemplaires généralement acceptées ou b) disposent d’un programme de réforme qui a été mis en place afin qu’ils adhèrent à ces pratiques. IHP+Results a ces données de sorte qu'il n'est pas nécessaire pour vous de répondre à cette question.",
"6G":  "Un cadre d’évaluation de la performance transparent, convenu conjointement et dont le suivi est assuré, est utilisé pour évaluer les progrès accomplis dans le secteur de la santé.",
"7G":  "Des évaluations mutuelles telles que les revues sectorielles annuelles conjointes en matière de santé ont été faites sur les progrès accomplis en ce qui concerne la mise en oeuvre d’engagements dans le secteur de la santé, notamment en ce qui concerne l’efficacité de l’aide.",
"8G":  "Données indiquant que la société civile est représentée activement dans les processus relatifs aux politiques dans le secteur de la santé, notamment la planification, la coordination et les mécanismes de revue dans le secteur de la santé. (s'il vous plaît cocher la case de nombreuses catégories, le cas échéant)",
}


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
        make_option('--gov',
            dest='gov',
            default=False,
            action='store_true',
            help='gov_output'),
        )
    output_transaction = True

    def handle(self, *args, **options):
        survey_file = xlrd.open_workbook(args[0])
        name = options['name']
        lang = options['lang']
        gov = options['gov']
        if not name:
            raise CommandError("Require a name for the survey")

        if lang!='fr':
            raise CommandError("'fr' is the only language currently supported")
        
        group = None
        survey= models.Survey.objects.get(name=name, project=models.Project.objects.get())
        questions = dict([(q.identifier,q) for q in survey.question_set.all()])
        questiongroup = dict([(q.name,q) for q in survey.questiongroup_set.all()])
        qg = survey.questiongroup_set.get(name="Additional questions")
        item,created = qg.questiongrouptranslation_set.get_or_create(lang=lang,defaults={'name':'Des questions supplémentaires'})
        item.name = 'Des questions supplémentaires'
        item.save()

        for q in survey.questiongroup_set.all():
            if q.name in group_text:
                g,created=q.questiongrouptranslation_set.get_or_create(lang=lang, defaults={'name':q.name,'help_text':group_text[q.name]})
                if not created:
                    g.help_text = group_text[q.name]
                    g.save()

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
        start_row = 7
        q_col = 3
        q_text = 4
        if gov:
            start_row = 6
            q_col = 1
            q_text = 2
        for row_num in xrange(start_row,sheet.nrows):
            row = sheet.row(row_num)
            indicator = row[0].value
            if not gov and indicator in questiongroup:
                g,created=questiongroup[indicator].questiongrouptranslation_set.get_or_create(lang=lang, defaults={'name':indicator,'help_text':row[1].value})
                if not created:
                    g.help_text = row[1].value
                    g.save()
                
            try:
                q_num = str(int(row[q_col].value))
                q = row[q_text].value
            except:
                pass

            question = questions[q_num]
            qt,created  = question.questiontranslation_set.get_or_create(lang=lang, defaults={'question':q})
            qt.question = q
            qt.save()
