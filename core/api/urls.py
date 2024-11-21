from rest_framework.routers import DefaultRouter

from .viewsets import ProductSearchViewSet


router = DefaultRouter()
router.register(r"products", ProductSearchViewSet, basename="products")