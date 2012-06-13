from django.contrib import admin
from ierg_results.models import Region, Country, Target, ExcelFile
from ierg_results.forms import ExcelFileAdminForm


class RegionAdmin(admin.ModelAdmin):
    list_display = ['__unicode__']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'region']


class TargetAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'target']


class ExcelFileAdmin(admin.ModelAdmin):
    form = ExcelFileAdminForm
    list_display = ['__unicode__', 'uploaded']
    readonly_fields = ['parse_log']


admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Target, TargetAdmin)
admin.site.register(ExcelFile, ExcelFileAdmin)

