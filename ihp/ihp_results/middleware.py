from django.db import connection
from django.conf import settings

from django.contrib.sites.models import Site
from django.http import HttpResponsePermanentRedirect
from django.core.urlresolvers import resolve
from django.core import urlresolvers
from django.utils.http import urlquote

import logging
log = logging.getLogger(__name__)

class DomainRedirectMiddleware(object):
    def process_request(self, request):
        host = request.get_host()
        site = Site.objects.get_current()

        if host == site.domain:
            return None

        ## Only redirect if the request is a valid path
        #try:
        #    # One issue here: won't work when using django.contrib.flatpages
        #    # TODO: Make this work with flatpages :-)
        #    resolve(request.path)
        #except urlresolvers.Resolver404:
        #    return None

        new_uri = '%s://%s%s%s' % (
                request.is_secure() and 'https' or 'http',
                site.domain,
                urlquote(request.path),
                (request.method == 'GET' and len(request.GET) > 0) and '?%s' % request.GET.urlencode() or ''
            )

        return HttpResponsePermanentRedirect(new_uri)
