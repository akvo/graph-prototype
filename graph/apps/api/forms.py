__author__ = 'arun'

from django import forms
from django.forms.models import inlineformset_factory
from .models import FileData, Chart, ChartSeries

class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = FileData
        exclude = ['title']


class ChartForm(forms.ModelForm):
    data = forms.ModelChoiceField(queryset=FileData.objects.all(), widget=forms.HiddenInput())
    #options = forms.CharField(widget=forms.HiddenInput())
    #type = forms.ChoiceField(choices=Chart.CHART_TYPE_CHOICES, widget=forms.RadioSelect())
    class Meta:
        model = Chart
        fields = ['title', 'type', 'data']


class ChartSeriesForm(forms.ModelForm):
    column = forms.ChoiceField(widget=forms.Select())
    axis = forms.ChoiceField(widget=forms.Select())
    class Meta:
        model = ChartSeries
        fields = ['column', 'filter', 'label']

ChartSeriesFormset = inlineformset_factory(Chart, ChartSeries)