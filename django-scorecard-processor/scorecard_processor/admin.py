from django.contrib import admin
from models import  DataSeries, DataSeriesGroup, Entity, EntityType, Survey, Question, ResponseSet, Response, Scorecard, Operation, OperationArgument, Project, ReportRun
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

admin.site.register(Question)
admin.site.register(Scorecard)
admin.site.register(ReportRun)

admin.site.register(DataSeriesGroup, DataSeriesGroupAdmin)
admin.site.register(Entity)
admin.site.register(EntityType)
admin.site.register(Project)

from forms import ArgumentForm
class OperationArgumentInline(admin.StackedInline):
    model = OperationArgument
    form = ArgumentForm
    related_lookup_fields = {
         'generic': [['instance_content_type', 'instance_id']],
    }
    sortable_field_name = "position"
    extra = 0

    def get_formset(self, request, obj = None,**kwargs):
        if obj:
            self.parent_obj = obj
            self.max_num = len(obj.plugin.argument_list)
            self.extra=self.max_num - obj.operationargument_set.count()
        else:
            parent = getattr(self,'parent_obj',None)
            if not parent:
                self.max_num = 0
        return super(OperationArgumentInline,self).get_formset(request, obj=obj, **kwargs)

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(OperationArgumentInline, self).formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'instance_content_type':
            if getattr(self,'parent_obj',None):
                field.queryset = field.queryset.filter(name__in=['question','operation'])
        return field


class OperationAdmin(admin.ModelAdmin):
    model = Operation
    list_filter = ('scorecard',)
    inlines = [OperationArgumentInline]
    classes = ('collapse open',)

admin.site.register(Operation, OperationAdmin)
