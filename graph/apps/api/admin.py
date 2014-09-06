from django.contrib import admin

from .models import FileData, Chart, ChartSeries


class FileDataAdmin(admin.ModelAdmin):
    pass
admin.site.register(FileData, FileDataAdmin)


class ChartAdmin(admin.ModelAdmin):
    pass
admin.site.register(Chart, ChartAdmin)


class ChartSeriesAdmin(admin.ModelAdmin):
    pass
admin.site.register(ChartSeries, ChartSeriesAdmin)
