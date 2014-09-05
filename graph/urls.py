from django.conf.urls.static import static
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from graph.apps.api.views import SpreadsheetListView, SpreadsheetDetailView, UploadView, ChartMetaView, ChartCreateView, ChartDetailView

admin.autodiscover()

urlpatterns = patterns('',
   # (r'', include('graph.apps.')),
    #url(r'^editor/', TemplateView.as_view(template_name='spreadsheet.html')),
    url(r'^/?$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^new/', UploadView.as_view(), name='spreadsheet-upload'),
    url(r'^ss/?$', SpreadsheetListView.as_view(), name="spreadsheet-list"),
    url(r'^ss/(?P<pk>\d+)?', SpreadsheetDetailView.as_view(), name='spreadsheet-detail'),
    url(r'api/chart/(?P<pk>\d+)/?$', ChartMetaView.as_view(), name='chart-definition'),
    url(r'^api/chart/(?P<pk>\d+)/data/$', 'graph.apps.api.views.xld', name='chart-data'),
    url(r'^api/chart/(?P<pk>\d+)/data/orient/(?P<orient>\w+)/$', 'graph.apps.api.views.xld', name='chart-data-orient'),
    url(r'^api/chart/(?P<pk>\d+)/data/orient/(?P<orient>\w+)/format/(?P<format>\w+)/$', 'graph.apps.api.views.xld', name='chart-data-orient-format'),
    url(r'^chart/new/?$', ChartCreateView.as_view(), name="chart-create"),
    url(r'^chart/(?P<pk>\d+)/?$', ChartDetailView.as_view(), name="chart-detail"),
    url(r'^chart/$', TemplateView.as_view(template_name='chart.html'), name='chart'),
    url(r'^api/nb/(?P<notebook>\w+)/(?P<var>\w+)/?', 'graph.apps.api.views.notebook_visualization', name="notebook-visualization"),
    url(r'^nb/?$', TemplateView.as_view(template_name="notebook_viewer.html"), name="notebook-viewer"),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
