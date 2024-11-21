from rest_framework import viewsets, response, mixins
from rest_framework.decorators import action
from core.models import Product
from core.api.serializers import ProductSearchSerializer
from core.pinecone import PineconeInterface
from core.openai_client import OpenAIClient
from core.cohere import Cohere
from core.api.filters import ProductFilter
from django_filters.rest_framework import DjangoFilterBackend

class ProductSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSearchSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        return self.queryset

    @action(detail=False, methods=['post'])
    def search(self, request):
        query = request.data.get('query')
        if not query:
            return response.Response({"error": "Query is required"}, status=400)

        # Get OpenAI response to formulate the best search string
        openai_client = OpenAIClient()
        openai_prompt = f"Formulate the best search string for the following user query: {query}"
        search_string = openai_client.get_response(openai_prompt)

        # Get embeddings for the formulated search string
        cohere = Cohere()
        query_embedding = cohere.embed([search_string])

        # Perform similarity search
        pinecone = PineconeInterface()
        limit = request.data.get('limit', 10)
        similar_products = pinecone.query(query_embedding, top_k=limit)

        # Sort matches by score in descending order
        sorted_matches = sorted(similar_products.get('matches', []), key=lambda x: x['score'], reverse=True)

        # Fetch product details
        product_ids = [match.id for match in sorted_matches]
        products = Product.objects.filter(pinecone_id__in=product_ids)
        serializer = ProductSearchSerializer(products, many=True)

        # Prepare product details for OpenAI prompt
        product_details = "\n".join([f"Title: {product.title}, Price: {product.price}, Stars: {product.stars}, Reviews: {product.reviews}" for product in products])

        # Get OpenAI response with product details
        openai_prompt = f"User query: {query}\n\nSimilar products:\n{product_details}\n\nProvide a response to the user including these product details."
        openai_response = openai_client.get_response(openai_prompt)

        return response.Response({
            "openai_response": openai_response,
            "products": serializer.data
        })
