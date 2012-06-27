from django.contrib import admin
from ierg_results.models import Region, Country, Indicator, ExcelFile
from ierg_results.forms import ExcelFileAdminForm


class RegionAdmin(admin.ModelAdmin):
    list_display = ['__unicode__']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'flag', 'region']
    readonly_fields = ['flag']


class IndicatorAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'target', 'parent']


class ExcelFileAdmin(admin.ModelAdmin):
    form = ExcelFileAdminForm
    list_display = ['__unicode__', 'uploaded']
    readonly_fields = ['parse_log']


admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Indicator, IndicatorAdmin)
admin.site.register(ExcelFile, ExcelFileAdmin)

