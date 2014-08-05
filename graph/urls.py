from django.conf.urls.static import static
from django.conf.urls import patterns, url, include
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib import admin
from graph.apps.api.views import SpreadsheetView, UploadView

admin.autodiscover()

urlpatterns = patterns('',
   # (r'', include('graph.apps.')),
    #url(r'^editor/', TemplateView.as_view(template_name='spreadsheet.html')),
    url(r'^/?$', TemplateView.as_view(template_name='index.html'), name='index'),
    url(r'^new/', UploadView.as_view(), name='upload'),
    url(r'^ss/(?P<pk>\d+)?', SpreadsheetView.as_view(), name='spreadsheet'),
    url(r'^data/(?P<pk>\d+)?', 'graph.apps.api.views.xld', name='data'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)
