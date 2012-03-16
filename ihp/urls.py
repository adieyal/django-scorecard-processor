from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    (r'^$', direct_to_template, {'template':'index.html'}),
    (r'^accounts/', include('django.contrib.auth.urls')),
    (r'^scorecard/', include('scorecard_processor.urls')),
    (r'^scorecard/entity/', include('ihp_results.entity_urls')),

    (r'^ihp_results/', include('ihp_results.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^grappelli/', include('grappelli.urls')),

    (r'^static/(?P<path>.*)$','django.views.static.serve',{'document_root': 'static'}),

)


