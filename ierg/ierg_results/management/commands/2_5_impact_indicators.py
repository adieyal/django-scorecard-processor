from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '2.5 Impact indicators'
    COLUM_NAME_ROW_STRING = "A4:R4"
    START_LINE = 4

    QUESTIONS_SC = [
        range(1, 7),
        range(7, 13),
        range(13, 18),
    ]


    def get_json(self, sheet, column_names, i):
        value = {}
        value['data'] = []

        for questions_sc in self.QUESTIONS_SC:
            questions = {}
            for j in questions_sc:
                questions[column_names[j]] = sheet.cell(row=i, column=j).value
            value['data'].append(questions)

        return simplejson.dumps(value)

