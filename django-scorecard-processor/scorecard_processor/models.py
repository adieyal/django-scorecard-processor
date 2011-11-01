#
#class DataSeries(models.Model):
#    name = models.CharField()
#
#class Survey(models.Model):
#    name = models.CharField()
#    project = models.ForeignKey(Project)
#    data_series = ManytoManyField(DataSeries) #Country, Year, Agency
#
#class Question(models.Model):
#    survey = models.ForeignKey(Survey)
#    identifier = models.CharField #1, 2a, 2b
#    question = models.TextField()
#
#class ResponseSet(models.Model):
#    survey = models.ForeignKey(Survey)
#    respondant = models.ForeignKey(User)
#    submission_date = models.DateTimeField(auto_now_add=True)
#    entity = models.ForeignKey(Entity)
#    data_series = ManytoManyField(DataSeries) #Country, Year, Agency
#    
#class Response(models.Model):
#    question = models.ForeignKey(Question)
#    response_set = models.ForeignKey(ResponseSet)
#    value = models.CharField()
#    valid = models.BooleanField #Has this been validated, and is a valid entry?
#    comment = models.TextField()
#
#class Transition(models.Model):
#        
