from django.db import models

# Create your models here.
class FileData(models.Model):
    file = models.FileField(upload_to=".")
    title = models.CharField(max_length=255, blank=True)
    created_on = models.DateField(auto_now_add=True)
    updated_on = models.DateField(auto_now=True)

