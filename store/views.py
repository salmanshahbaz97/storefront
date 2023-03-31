from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend  

from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Product, Collection, OrderItem, Review, Cart, CartItem
from .serializer import ProductSerializer, CollectionSerializer, ReviewSerializer, CartSerializer

from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.object.filter(collection_id = self.kwargs['pk']).count() > 0:
            return Response({'error': 'Collection cannot be deleted because it include one or more products'})
        return super().destroy(request, *args, **kwargs)
    

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']

    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it in one or more order items'})
        return super().destroy(request, *args, **kwargs)
    

class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id = self.kwargs['product_pk'])
    

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer