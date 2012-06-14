from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '4.1 Total Health Expenditure'
    SURVEY_NAME = 'Total Health Expenditure'
    IDENTIFIER = '4.1'
    QUESTION = 'Total health expenditure per capita was tracked during the two preceding years, by financing source'
    COLUM_NAME_ROW_STRING = "A4:G4"
    RATING_COLUMN = 1
    VALUE_COLUMNS = [2, 3, 6]
    VALUE_COLUMNS_2 = [4, 5, 6]
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        for j in self.VALUE_COLUMNS:
            value_index = column_names[j].replace('Source1/2', 'Source 1')
            value[value_index] = sheet.cell(row=i, column=j).value
        for j in self.VALUE_COLUMNS_2:
            value_index = column_names[j].replace('Source1/2', 'Source 2')
            value[value_index] = sheet.cell(row=i, column=j).value
        return simplejson.dumps(value)

