from django.db import models
from jsonfield import JSONField

# Create your models here.
class FileData(models.Model):
    file = models.FileField(upload_to=".")
    title = models.CharField(max_length=255, blank=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

class Chart(models.Model):
    CHART_TECH_WIJMO = 'W'
    CHART_TECH_VEGA = 'V'
    CHART_TECH_CHOICES = (
        (CHART_TECH_WIJMO, 'Wijmo'),
        (CHART_TECH_VEGA, 'Vega')
    )

    CHART_TYPE_LINE = 'L'
    CHART_TYPE_BAR = 'B'
    CHART_TYPE_PIE = 'P'
    CHART_TYPE_CHOICES = (
        (CHART_TYPE_LINE, 'Line'),
        (CHART_TYPE_BAR, 'Bar'),
        (CHART_TYPE_PIE, 'Pie')
    )

    tech = models.CharField(max_length=2, choices=CHART_TECH_CHOICES)
    type = models.CharField(max_length=1, choices=CHART_TYPE_CHOICES)
    title = models.CharField(max_length=32)
    data = models.ForeignKey('FileData')
    options = JSONField(blank=True)

class ChartSeries(models.Model):
    chart = models.ForeignKey('Chart', related_name='series')
    column = models.CharField(max_length=32)
    axis = models.CharField(max_length=2)
    label = models.CharField(max_length=32, blank=True)
    filter = models.CharField(max_length=255, blank=True)
