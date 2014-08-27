__author__ = 'arun'

from rest_framework import serializers
import pandas as pd
from .models import Chart, ChartSeries

class FileDataSerializer(serializers.RelatedField):
    def to_native(self, value):
        xf = pd.ExcelFile(value.file.path)
        xld = xf.parse(xf.sheet_names[0])
        return xld.to_json()

class ChartSeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChartSeries
        fields = ['column', 'filter']

class ChartSerializer(serializers.ModelSerializer):
    series = ChartSeriesSerializer(many=True)
    #data = FileDataSerializer() #The whole field is a string, need to look at custom renderers

    class Meta:
        model = Chart
        fields = ['series', 'tech', 'type', 'title']