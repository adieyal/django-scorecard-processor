from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class DataSeries(models.Model):
    name = models.CharField()

class Survey(models.Model):
    name = models.CharField()
    project = models.ForeignKey(Project)
    data_series = ManytoManyField(DataSeries) #Country, Year, Agency

class Question(models.Model):
    survey = models.ForeignKey(Survey)
    identifier = models.CharField #1, 2a, 2b
    question = models.TextField()

    def get_value(self, data_series=[], responseset_set=[]):
        return ''

class ResponseSet(models.Model):
    survey = models.ForeignKey(Survey)
    respondant = models.ForeignKey(User)
    submission_date = models.DateTimeField(auto_now_add=True)
    entity = models.ForeignKey(Entity)
    data_series = ManytoManyField(DataSeries) #Country, Year, Agency
    
class Response(models.Model):
    question = models.ForeignKey(Question)
    response_set = models.ForeignKey(ResponseSet)
    value = models.CharField()
    valid = models.BooleanField #Has this been validated, and is a valid entry?
    comment = models.TextField()

class Transition(models.Model):
    method = models.CharField()
    data_series = models.ManyToManyField(DataSeries)
    results_by_data_series = models.BooleanField()
    results_by_respondant = models.BooleanField()
    result_fold_function = models.CharField()

    def get_values(self, response_set, data_series):
        """ Outputs a value from the transition, applying the method to the
        arguments"""
        return ''

class TransitionArgument(models.Model):
    """Arguments need to be ordered and they may be specific question
    responses, or outputs from transitions""" 

    order = models.IntegerField()
    transition = models.ForeignKey(Transition)
    instance_content_type = models.ForeignKey(ContentType)
    instance_id = models.PositiveIntegerField()
    instance = generic.GenericForeignKey('sender_content_type', 'sender_id')

    

# transition('add_values', Question(1), DataSeries(2011), DataSeries(South Africa)).get_values()
