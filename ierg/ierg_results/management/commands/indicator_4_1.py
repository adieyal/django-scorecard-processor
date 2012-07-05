from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '4.1 Total Health Expenditure'
    SURVEY_NAME = 'Total Health Expenditure'
    COLUM_NAME_ROW_STRING = "A4:M4"
    START_LINE = 4

    IDENTIFIER = '4.1'
    QUESTION = 'Total health expenditure per capita was tracked during the two preceding years, by financing source'


    def get_json(self, sheet, column_names, i):
        print column_names
        value = {}
        rating_column = 1
        value_column = [8, 9, 12]
        value_column_2 = [10, 11, 12]

        value['Yes/No'] = sheet.cell(row=i, column=rating_column).value
        value['Yes/No'] = 'No data' if value['Yes/No'] is None else value['Yes/No']
        for j in value_column:
            value_index = column_names[j].replace('Source 3/4', 'Source 3')
            value[value_index] = sheet.cell(row=i, column=j).value
        for j in value_column_2:
            value_index = column_names[j].replace('Source 3/4', 'Source 4')
            value[value_index] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

