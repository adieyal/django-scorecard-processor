from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '1.3MaternalDeathReviews'
    COLUM_NAME_ROW_STRING = "A6:W6"
    START_LINE = 6
    FINISH_LINE = 81


    def get_json(self, sheet, column_names, i):
        value = {}
        for j in column_names:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

