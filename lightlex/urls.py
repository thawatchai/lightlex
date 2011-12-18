# vim: ai ts=4 sts=4 et sw=4

import os
import settings
from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        (r'^lightlex/admin[/]?(.*)', admin.site.root),
        (r'^(?!lightlex)', include('lightlex.lexitron.urls')),
        )

if settings.DEBUG:
    urlpatterns += patterns('',
            (r'^lightlex-media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '%s/../lightlex-media' % os.path.dirname(__file__)}),
            )
