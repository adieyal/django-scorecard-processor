from django.contrib import admin
from ierg_results.models import Region, Country, ExcelFile


class RegionAdmin(admin.ModelAdmin):
    list_display = ['__unicode__']


class CountryAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'region']


class ExcelFileAdmin(admin.ModelAdmin):
    list_display = ['__unicode__', 'uploaded']
    readonly_fields = ['parse_log']


admin.site.register(Region, RegionAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(ExcelFile, ExcelFileAdmin)

