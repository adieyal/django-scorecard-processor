from django.conf.urls.defaults import *

urlpatterns = patterns('scorecard_processor.views',
    (r'^$', 'index'),
)

