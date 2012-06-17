from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    SHEET_NAME = '4.1 Total Health Expenditure'
    SURVEY_NAME = 'Total Health Expenditure'
    COLUM_NAME_ROW_STRING = "A4:G4"
    START_LINE = 4

    IDENTIFIER = '4.1'
    QUESTION = 'Total health expenditure per capita was tracked during the two preceding years, by financing source'


    def get_json(self, sheet, column_names, i):
        value = {}
        rating_column = 1
        value_column = [2, 3, 6]
        value_column_2 = [4, 5, 6]

        value[column_names[rating_column]] = sheet.cell(row=i, column=rating_column).value
        for j in value_column:
            value_index = column_names[j].replace('Source1/2', 'Source 1')
            value[value_index] = sheet.cell(row=i, column=j).value
        for j in value_column_2:
            value_index = column_names[j].replace('Source1/2', 'Source 2')
            value[value_index] = sheet.cell(row=i, column=j).value

        return simplejson.dumps(value)

