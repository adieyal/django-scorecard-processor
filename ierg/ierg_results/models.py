from django.db import models
from django.core.management import call_command


class ExcelFile(models.Model):
    excel_file = models.FileField(upload_to='excel_files', max_length=255)
    parse_log = models.TextField(blank=True)
    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded']
        app_label = 'ierg_results'

    def __unicode__(self):
        return '%s' % self.excel_file.name

    def save(self, *args, **kwargs):
        new = False if self.id else True
        super(ExcelFile, self).save(*args, **kwargs)
        if new:
            call_command('1_1_birth_registration', file_path=self.excel_file.path,
                survey_name='BirthRegistration', excel_file_id=self.id)
            call_command('1_2_death_registration', file_path=self.excel_file.path,
                survey_name='DeathRegistration', excel_file_id=self.id)
            call_command('1_3_maternal_death_reviews', file_path=self.excel_file.path,
                survey_name='MaternalDeathReviews', excel_file_id=self.id)
            call_command('1_4_cod', file_path=self.excel_file.path,
                survey_name='COD', excel_file_id=self.id)
            call_command('1_5_qoc', file_path=self.excel_file.path,
                survey_name='QoC', excel_file_id=self.id)
            call_command('1_7_crvs_improvement', file_path=self.excel_file.path,
                survey_name='CRVSImprovement', excel_file_id=self.id)
            call_command('2_1_health_info', file_path=self.excel_file.path,
                survey_name='HealthInfo', excel_file_id=self.id)
            call_command('2_2_coverage_indicators', file_path=self.excel_file.path,
                survey_name='CoverageIndicators', excel_file_id=self.id)
            call_command('2_3_impact_indicators', file_path=self.excel_file.path,
                survey_name='ImpactIndicators', excel_file_id=self.id)
            call_command('3_1_ehealth_strategy', file_path=self.excel_file.path,
                survey_name='EhealthStrategy', excel_file_id=self.id)
            call_command('3_2_web_based_reporting', file_path=self.excel_file.path,
                survey_name='WebBasedReporting', excel_file_id=self.id)
            call_command('4_1_total_health_expenditure', file_path=self.excel_file.path,
                survey_name='TotalHealthExpenditure', excel_file_id=self.id)
            call_command('4_2_nha_conducted', file_path=self.excel_file.path,
                survey_name='NhaConducted', excel_file_id=self.id)
            call_command('4_3_rmnch_expenditure', file_path=self.excel_file.path,
                survey_name='RmnchExpenditure', excel_file_id=self.id)
            call_command('5_1_financial_reporting_system', file_path=self.excel_file.path,
                survey_name='FinancialReportingSystem', excel_file_id=self.id)
            call_command('6_1_reviews_of_health_spending', file_path=self.excel_file.path,
                survey_name='ReviewsOfHealthSpending', excel_file_id=self.id)
            call_command('7_1_reviews_of_performance', file_path=self.excel_file.path,
                survey_name='ReviewsOfPerformance', excel_file_id=self.id)
            call_command('8_1_performance_report_public', file_path=self.excel_file.path,
                survey_name='PerformanceReportPublic', excel_file_id=self.id)

