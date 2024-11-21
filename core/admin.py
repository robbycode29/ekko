from django.contrib import admin
from .models import ExcelFile
from .forms import ExcelFileForm
import pandas as pd
from io import BytesIO

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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # Process the uploaded file
        file = form.cleaned_data['file']
        file.seek(0)
        df = pd.read_csv(BytesIO(file.read()))

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
                pinecone_id=vectors[0].get('id'),
                title=df.iloc[embeddings.index(embedding)].get('title', ''),
                img_url=df.iloc[embeddings.index(embedding)].get('imgUrl', ''),
                product_url=df.iloc[embeddings.index(embedding)].get('productURL', ''),
                stars=df.iloc[embeddings.index(embedding)].get('stars', 0),
                reviews=df.iloc[embeddings.index(embedding)].get('reviews', 0),
                price=df.iloc[embeddings.index(embedding)].get('price', 0)
            )
