from django.conf import settings
from django.conf.urls import patterns, include, url

from flight_search.apps.core.views import FlightSearchFormView, FlightSearchResultsView

urlpatterns = patterns('',
    url(r'^$', FlightSearchFormView.as_view(), name='home'),
    url(r'^search/$', FlightSearchResultsView.as_view(), name='search_results'),
    # url(r'^locations_autocomplete/$', "flight_search.apps.core.views.locations_autocomplete", name='locations_autocomplete'),
)

urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT,
    }),
)

urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT,
    }),
)
