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
            call_command('1_1_indicator', file_path=path, excel_file_id=fid)
            call_command('1_2_indicator', file_path=path, excel_file_id=fid)
            call_command('1_3_indicator', file_path=path, excel_file_id=fid)
            call_command('1_3_1_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('1_3_2_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('1_3_3_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('1_3_4_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('1_3_5_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('1_5_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('1_6_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('1_7_indicator', file_path=path, excel_file_id=fid)
            call_command('1_7_1_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_1_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_1_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_2_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_3_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_4_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_5_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_6_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_7_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_2_8_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('2_3_indicator', file_path=path, excel_file_id=fid)
            call_command('3_1_indicator', file_path=path, excel_file_id=fid)
            call_command('3_1_1_sub-indicator', file_path=path, excel_file_id=fid)
            call_command('3_2_indicator', file_path=path, excel_file_id=fid)
            call_command('4_1_indicator', file_path=path, excel_file_id=fid)
            call_command('4_2_indicator', file_path=path, excel_file_id=fid)
            call_command('4_3_indicator', file_path=path, excel_file_id=fid)
            call_command('5_1_indicator', file_path=path, excel_file_id=fid)
            call_command('6_1_indicator', file_path=path, excel_file_id=fid)
            call_command('7_1_indicator', file_path=path, excel_file_id=fid)
            call_command('8_1_indicator', file_path=path, excel_file_id=fid)

