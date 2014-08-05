from django.shortcuts import render
from django.views.generic import View, FormView, TemplateView

from django.conf import settings
from django.core.urlresolvers import reverse
import os

from .forms import ExcelFileForm
from .models import FileData

# Create your views here.
class UploadView(FormView):
    form_class = ExcelFileForm
    template_name = "upload.html"

    def __init__(self):
        super(self.__class__, self).__init__()
        self.id = None

    def get_success_url(self):
        return reverse('spreadsheet', kwargs={'pk': self.id})

    def form_valid(self, form):
        obj = form.save(commit=True)
        self.id = obj.id
        return super(self.__class__, self).form_valid(form)

class SpreadsheetView(TemplateView):
    template_name = "spreadsheet.html"

    def get_context_data(self, **kwargs):
        ctx = super(self.__class__, self).get_context_data(**kwargs)
        if kwargs['pk']:
            ctx['data'] = FileData.objects.get(pk=kwargs['pk'])
        else:
            ctx['sheets'] = FileData.objects.all()
        return ctx

import pandas as pd
from django.http import HttpResponse

def xld(request, pk=None):
    if not pk:
        return HttpResponse("{\"message\": \"No spreadsheet selected or uploaded\"}", content_type="application/json")

    obj = FileData.objects.get(pk=pk)
    xf = pd.ExcelFile(obj.file.path)
    xld = xf.parse(xf.sheet_names[0])
    return HttpResponse(xld.to_json(), content_type="application/json")