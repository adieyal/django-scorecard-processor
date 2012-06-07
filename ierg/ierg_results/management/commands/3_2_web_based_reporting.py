from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '3.2 Web based reporting'
    COLUM_NAME_ROW_STRING = "A4:E4"
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        for j in column_names:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

