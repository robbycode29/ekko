import cohere
from bot.settings import COHERE_TOKEN


class Cohere:
    def __init__(self):
        self.client = cohere.Client(COHERE_TOKEN)

    def embed(self, texts):
        cohere_response = self.client.embed(
            model='embed-english-v3.0',
            texts=texts,
            input_type='classification',
            truncate='NONE'
        )
        return cohere_response.embeddings
