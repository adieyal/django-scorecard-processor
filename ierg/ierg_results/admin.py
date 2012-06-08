from django.contrib import admin
from ierg_results.models import ExcelFile


class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'uploaded']
    readonly_fields = ['parse_log']


admin.site.register(ExcelFile, ExcelFileAdmin)

