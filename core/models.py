from django.db import models


class ExcelFile(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    offset = models.IntegerField(default=0)
    limit = models.IntegerField(default=1000)


class Product(models.Model):
    pinecone_id = models.CharField(null=True, blank=True)
    title = models.CharField(null=True, blank=True)
    img_url = models.CharField(null=True, blank=True)
    product_url = models.CharField(null=True, blank=True)
    stars = models.FloatField()
    reviews = models.IntegerField()
    price = models.FloatField()
