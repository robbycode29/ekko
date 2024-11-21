from django.db import models


class ExcelFile(models.Model):
    file = models.FileField(upload_to='excel_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    offset = models.IntegerField(default=0)
    limit = models.IntegerField(default=1000)


class Product(models.Model):
    pinecone_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    img_url = models.CharField(max_length=255)
    product_url = models.CharField(max_length=255)
    stars = models.FloatField()
    reviews = models.IntegerField()
    price = models.FloatField()
