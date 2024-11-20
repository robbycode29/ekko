from django.db import models

class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    offset = models.IntegerField(default=0)
    limit = models.IntegerField(default=1000)
