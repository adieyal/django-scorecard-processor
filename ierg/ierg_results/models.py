from django.db import models
from django.core.management import call_command
from scorecard_processor.models import Entity, DataSeries, Response, ResponseSet, Question, Survey


EXCEL_FILES_SECTION = 'excel_files'


class Region(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
        app_label = 'ierg_results'

    def __unicode__(self):
        return '%s' % self.name


class Country(models.Model):
    name = models.CharField(max_length=255)
    flag = models.CharField(max_length=255, blank=True)
    region = models.ForeignKey(Region, related_name='countries')

    class Meta:
        ordering = ['name']
        verbose_name_plural = "countries"
        app_label = 'ierg_results'

    def __unicode__(self):
        return '%s' % self.name


class Indicator(models.Model):
    indicator = models.CharField(max_length=10)
    target = models.CharField(max_length=10)

    class Meta:
        ordering = ['indicator']
        app_label = 'ierg_results'

    def __unicode__(self):
        return '%s' % self.indicator


class ExcelFile(models.Model):
    excel_file = models.FileField(upload_to=EXCEL_FILES_SECTION, max_length=255)
    parse_log = models.TextField(blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded']
        app_label = 'ierg_results'

    def __unicode__(self):
        return '%s' % self.excel_file.name.replace(EXCEL_FILES_SECTION+'/', '')

    def save(self, *args, **kwargs):
        new = False if self.id else True
        super(ExcelFile, self).save(*args, **kwargs)
        if new:
            Entity.objects.all().delete()
            DataSeries.objects.all().delete()
            Response.objects.all().delete()
            ResponseSet.objects.all().delete()
            Question.objects.all().delete()
            Survey.objects.all().delete()

            fid = self.id
            path = self.excel_file.path
            call_command('indicator_1_1', file_path=path, excel_file_id=fid)
            call_command('indicator_1_2', file_path=path, excel_file_id=fid)
            call_command('indicator_1_3', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_1_3_1', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_1_3_2', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_1_3_3', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_1_3_4', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_1_3_5', file_path=path, excel_file_id=fid)
            call_command('indicator_1_5', file_path=path, excel_file_id=fid)
            call_command('indicator_1_6', file_path=path, excel_file_id=fid)
            call_command('indicator_1_7', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_1_7_1', file_path=path, excel_file_id=fid)
            call_command('indicator_2_1', file_path=path, excel_file_id=fid)
            call_command('indicator_2_2', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_1', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_2', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_3', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_4', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_5', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_6', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_7', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_2_2_8', file_path=path, excel_file_id=fid)
            call_command('indicator_2_3', file_path=path, excel_file_id=fid)
            call_command('indicator_3_1', file_path=path, excel_file_id=fid)
            call_command('sub-indicator_3_1_1', file_path=path, excel_file_id=fid)
            call_command('indicator_3_2', file_path=path, excel_file_id=fid)
            call_command('indicator_4_1', file_path=path, excel_file_id=fid)
            call_command('indicator_4_2', file_path=path, excel_file_id=fid)
            call_command('indicator_4_3', file_path=path, excel_file_id=fid)
            call_command('indicator_5_1', file_path=path, excel_file_id=fid)
            call_command('indicator_6_1', file_path=path, excel_file_id=fid)
            call_command('indicator_7_1', file_path=path, excel_file_id=fid)
            call_command('indicator_8_1', file_path=path, excel_file_id=fid)

