from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '3.1 eHealth strategy'
    SURVEY_NAME = 'eHealth strategy'
    IDENTIFIER = '3.1.1'
    QUESTION = 'Policy implemented'
    COLUM_NAME_ROW_STRING = "A4:I4"
    VALUE_COLUMNS = xrange(3, 6)
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        for j in self.VALUE_COLUMNS:
            value_index = column_names[j].replace('Source 1 and 2', 'Source 2')
            value[value_index] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

