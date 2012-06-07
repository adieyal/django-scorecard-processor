from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '3.1 eHealth strategy'
    COLUM_NAME_ROW_STRING = "A4:F4"
    START_LINE = 4

    YES_NO_SC = 1
    QUESTIONS_SC = [
        range(2, 3),
        range(3, 5),
    ]
    SOURCE_SC = 5


    def get_json(self, sheet, column_names, i):
        value = {}

        value[column_names[self.YES_NO_SC]] = sheet.cell(row=i,
            column=self.YES_NO_SC).value
        value[column_names[self.SOURCE_SC]] = sheet.cell(row=i,
            column=self.SOURCE_SC).value

        value['data'] = []
        for questions_sc in self.QUESTIONS_SC:
            questions = {}
            for j in questions_sc:
                questions[column_names[j]] = sheet.cell(row=i, column=j).value
            value['data'].append(questions)

        return simplejson.dumps(value)

