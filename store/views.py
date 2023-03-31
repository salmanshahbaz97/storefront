from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import Http404

from .models import Product, Collection, OrderItem
from .serializer import ProductSerializer, CollectionSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, mixins
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly


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
    
    def get_serializer_context(self):
        return {'request': self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=self.kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted because it in one or more order items'})
        return super().destroy(request, *args, **kwargs)