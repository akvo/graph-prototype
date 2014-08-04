__author__ = 'arun'

from django import forms
from .models import FileData

class ExcelFileForm(forms.ModelForm):
    class Meta:
        model = FileData
        exclude = ['title']