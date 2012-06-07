from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '2.4 Coverage indicators'
    COLUM_NAME_ROW_STRING = "A4:AA4"
    START_LINE = 4

    YES_NO_SC = 1
    DISAGGREGATIONS_SC = 2
    QUESTIONS_SC = [
        range(3, 6),
        range(6, 9),
        range(9, 12),
        range(12, 15),
        range(15, 18),
        range(18, 21),
        range(21, 24),
        range(24, 27),
    ]


    def get_json(self, sheet, column_names, i):
        value = {}

        value[column_names[self.YES_NO_SC]] = sheet.cell(row=i,
            column=self.YES_NO_SC).value
        value[column_names[self.DISAGGREGATIONS_SC]] = sheet.cell(row=i,
            column=self.DISAGGREGATIONS_SC).value
            
        value['data'] = []
        for questions_sc in self.QUESTIONS_SC:
            questions = {}
            for j in questions_sc:
                questions[column_names[j]] = sheet.cell(row=i, column=j).value
            value['data'].append(questions)

        return simplejson.dumps(value)

