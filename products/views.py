from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['category__name','name','user__username']


