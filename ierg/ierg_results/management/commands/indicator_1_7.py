from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '1.7CRVSimprovement'
    SURVEY_NAME = 'CRVS improvement'
    COLUM_NAME_ROW_STRING = "A4:O4"
    START_LINE = 4

    IDENTIFIER = '1.7'
    QUESTION = 'CRVS improvement plan approved by country government in place'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1
        value_column = xrange(6, 9)
        value_column_2 = 12

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']
        for j in value_column:
            value[column_names[j]] = sheet.cell(row=i, column=j).value
        value[column_names[value_column_2]] = sheet.cell(row=i, column=value_column_2).value

        return simplejson.dumps(value)

