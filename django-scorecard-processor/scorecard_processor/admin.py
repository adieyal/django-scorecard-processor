from django.contrib import admin
from models import  DataSeries, DataSeriesGroup, Entity, Survey, Question, ResponseSet, Response, Scorecard, Operation, OperationArgument, Project, ReportRun
from django.forms.models import BaseInlineFormSet 

class QuestionInline(admin.StackedInline):
    model = Question

class SurveyAdmin(admin.ModelAdmin):
    model = Survey
    inlines = [QuestionInline]

class DataSeriesInline(admin.TabularInline):
    model = DataSeries

class DataSeriesGroupAdmin(admin.ModelAdmin):
    model = DataSeriesGroup
    list_display = ('name', 'project',)
    list_filter = ('project',)
    inlines = [DataSeriesInline]

class ResponseInline(admin.StackedInline):
    model = Response

class ResponseSetAdmin(admin.ModelAdmin):
    model = ResponseSet
    inlines = [ResponseInline]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(ResponseSet, ResponseSetAdmin)

admin.site.register(Scorecard)
admin.site.register(ReportRun)
admin.site.register(Operation)
admin.site.register(OperationArgument)

admin.site.register(DataSeriesGroup, DataSeriesGroupAdmin)
admin.site.register(Entity)
admin.site.register(Project)
