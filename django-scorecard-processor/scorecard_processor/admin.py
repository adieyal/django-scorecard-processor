from django.contrib import admin
from models import  DataSeries, Entity, Survey, Question, ResponseSet, Response, Scorecard, Indicator, OperationArgument, Project
from django.forms.models import BaseInlineFormSet 

class QuestionInline(admin.StackedInline):
    model = Question

class SurveyAdmin(admin.ModelAdmin):
    model = Survey
    inlines = [QuestionInline]

class ResponseInline(admin.StackedInline):
    model = Response

class ResponseSetAdmin(admin.ModelAdmin):
    model = ResponseSet
    inlines = [ResponseInline]


admin.site.register(Survey, SurveyAdmin)
admin.site.register(ResponseSet, ResponseSetAdmin)

admin.site.register(Scorecard)
admin.site.register(Indicator)
admin.site.register(OperationArgument)

admin.site.register(DataSeries)
admin.site.register(Entity)
admin.site.register(Project)
