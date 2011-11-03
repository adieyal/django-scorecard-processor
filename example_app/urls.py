from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^example_app/', include('example_app.foo.urls')),
    (r'^$', direct_to_template, {'template':'index.html'}),
    (r'^account/', include('django.contrib.auth.urls')),
    (r'^scorecard/', include('scorecard_processor.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
