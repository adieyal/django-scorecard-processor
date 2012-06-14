from django.utils import simplejson
from ierg_results.management.commands.ierg_command import IergCommand


class Command(IergCommand):
    #TODO: We can get this from option or database later
    SHEET_NAME = '3.2 Web based reporting'
    SURVEY_NAME = 'Web based reporting'
    IDENTIFIER = '3.2'
    QUESTION = 'All districts are part of a national web based system to report health data and receive feedback'
    COLUM_NAME_ROW_STRING = "A4:E4"
    RATING_COLUMN = 1
    START_LINE = 4
    FINISH_LINE = 79


    def get_json(self, sheet, column_names, i):
        value = {}
        value[column_names[self.RATING_COLUMN]] = sheet.cell(row=i, column=self.RATING_COLUMN).value
        return simplejson.dumps(value)

