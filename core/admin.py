from django.contrib import admin
from .models import ExcelFile
from .forms import ExcelFileForm
import pandas as pd

from .cohere import Cohere
from .pinecone import PineconeInterface

@admin.register(ExcelFile)
class ExcelFileAdmin(admin.ModelAdmin):
    form = ExcelFileForm

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

        # Save embeddings to Pinecone
        pinecone = PineconeInterface()
        pinecone.upsert(embeddings)

