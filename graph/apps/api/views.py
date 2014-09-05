from django.shortcuts import render
from django.views.generic import View, FormView, TemplateView, ListView, DetailView, CreateView

from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import redirect

from django.http import Http404, HttpResponseServerError

from rest_framework.views import APIView
from rest_framework.response import Response

import os

from .forms import ExcelFileForm, ChartForm, ChartSeriesFormset
from .models import FileData, Chart
from .serializers import ChartSerializer

# Create your views here.
class UploadView(FormView):
    form_class = ExcelFileForm
    template_name = "upload.html"

    def __init__(self):
        super(self.__class__, self).__init__()
        self.id = None

    def get_success_url(self):
        return reverse('spreadsheet-detail', kwargs={'pk': self.id})

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

class SpreadsheetListView(ListView):
    model = FileData
    template_name = "api/spreadsheet_list.html"
    context_object_name = "sheets"

class SpreadsheetDetailView(DetailView):
    template_name = "api/spreadsheet_detail.html"
    context_object_name = "sheet"
    model = FileData

    def get_context_data(self, **kwargs):
        ctx = super(self.__class__, self).get_context_data(**kwargs)
        ctx['chart_form'] = ChartForm(initial={'data': self.object})
        ctx['formset'] = ChartSeriesFormset()
        return ctx

class ChartCreateView(CreateView):
    form_class = ChartForm
    template_name = "api/chart_create.html"

    def get_success_url(self):
        return reverse("chart-detail", kwargs= {'pk':self.object.id} )

    def form_valid(self, form):
        formset = ChartSeriesFormset(self.request.POST)
        self.object = form.save()
        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super(ChartCreateView, self).form_valid(form)

class ChartDetailView(DetailView):
    template_name = "api/chart_detail.html"
    model = Chart
    context_object_name = "chart"

class ChartMetaView(APIView):
    def get_object(self, pk):
        try:
            return Chart.objects.get(pk=pk)
        except Chart.DoesNotExist:
            raise Http404

    def get(self, request, **kwargs):
        chart = self.get_object(kwargs['pk'])
        serializer = ChartSerializer(chart)
        return Response(serializer.data)

import pandas as pd
from django.http import HttpResponse

def xld(request, pk=None, orient='records', format='json'):
    try:
        obj = FileData.objects.get(pk=pk)
    except Chart.DoesNotExist:
        return Http404

    xf = pd.ExcelFile(obj.file.path)
    xld = xf.parse(xf.sheet_names[0])
    return HttpResponse(xld.to_json(orient=orient, date_format='iso'), content_type="application/json")

def chart_data(request, pk):
    try:
        chart = Chart.objects.get(pk=pk)
    except Chart.DoesNotExist:
        return Http404

    xf = pd.ExcelFile(chart.data.file.path)
    xld = xf.parse(xf.sheet_names[0])
    return HttpResponse(xld.to_json(), content_type="application/json")

def chart_create(request):
    form = ChartForm(request.POST)
    formset = ChartSeriesFormset(request.POST)
    if form.is_valid():
        print "form is valid"

    return redirect("index")

import json
import imp

def notebook_visualization(request, notebook, var):
    nb_path = os.path.join(settings.ROOT_DIR, "{notebook}.ipynb".format(notebook=notebook))
    if not os.path.exists(nb_path):
        raise Http404
    nb = json.load(open(nb_path))
    code = []
    for cell in nb["worksheets"][0]["cells"]:
        if cell["cell_type"] == "code":
            code.extend([ x if x.endswith("\n") else x + "\n" for x in cell["input"]])
    try:
        nbmod = imp.new_module(notebook)
        exec ''.join(code) in nbmod.__dict__
    except Exception as e:
        return HttpResponseServerError(content=e)

    try:
        return HttpResponse(nbmod.__dict__[var].to_json(), content_type="application/json")
    except KeyError:
        raise Http404