from django import forms
from ierg_results.models import ExcelFile


class ExcelFileAdminForm(forms.ModelForm):

    class Meta:
        model = ExcelFile

    def clean_excel_file(self):
        excel_file = self.cleaned_data['excel_file']
        ext = excel_file.name.rsplit('.', 1)[-1]
        if ext != 'xls' and ext != 'xlsx':
            raise forms.ValidationError('Invalid file format.')
        return excel_file

