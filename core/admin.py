from django.contrib import admin
from .models import ExcelFile
from .forms import ExcelFileForm
import pandas as pd
import os

from .cohere import Cohere
from .pinecone import PineconeInterface
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'stars', 'reviews', 'price')
    search_fields = ('title',)

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    form = ExcelFileForm

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            if obj.file and os.path.isfile(obj.file.path):
                os.remove(obj.file.path)
        queryset.delete()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Process the uploaded file
        df = pd.read_csv(obj.file.path)

        # Take sample of the data
        offset = obj.offset
        limit = obj.limit
        df = df.iloc[offset:offset + limit]

        texts = df['title'].tolist()

        # Get embeddings
        cohere = Cohere()
        embeddings = cohere.embed(texts)

        # Save embeddings to Pinecone and DB
        pinecone = PineconeInterface()
        for embedding in embeddings:
            vectors = pinecone.upsert([embedding])
            Product.objects.create(
                pinecone_id=vectors[0]['id'],
                title=df.iloc[embeddings.index(embedding)]['title'],
                img_url=df.iloc[embeddings.index(embedding)]['imgUrl'],
                product_url=df.iloc[embeddings.index(embedding)]['productURL'],
                stars=df.iloc[embeddings.index(embedding)]['stars'],
                reviews=df.iloc[embeddings.index(embedding)]['reviews'],
                price=df.iloc[embeddings.index(embedding)]['price']
            )
