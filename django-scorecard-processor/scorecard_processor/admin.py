from django.contrib import admin
from models import  DataSeries, Entity, Survey, Question, ResponseSet, Response, Scorecard, Operation, OperationArgument

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(ResponseSet)
admin.site.register(Response)

admin.site.register(Scorecard)
admin.site.register(Operation)
admin.site.register(OperationArgument)

admin.site.register(DataSeries)
admin.site.register(Entity)
