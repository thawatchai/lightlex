from django.conf.urls.defaults import *

urlpatterns = patterns('lightlex.lexitron.views',
        (r'^$', 'lookup'),
        (r"^(?P<lookup_str>.+)$", 'lookup'),
        )
