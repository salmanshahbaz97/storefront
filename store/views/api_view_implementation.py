from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import Http404

from store.models import Product, Collection
from store.serializer import ProductSerializer, CollectionSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, mixins
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class CollectionList(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()   
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionDetail(APIView):
    """
    Retrieve, update or delete a collection instance.
    """
    def get_object(self, pk):
        try:
            return Collection.objects.annotate(products_count=Count('products')).get(pk=pk)
        except Collection.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    def put(self, request, pk):
        collection = self.get_object(pk)
        serializer = CollectionSerializer(collection, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        collection = self.get_object(pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it include one or more products'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductList(ListCreateAPIView):
    queryset = Product.objects.select_related('collection').all().order_by('-id')

    serializer_class = ProductSerializer
    
    def get_serializer_context(self):
        return {'request': self.request}


@api_view()
def product_detail(request, pk):
    try:
        product = get_object_or_404(Product, pk = pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    


class CollectionList(ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products')).all()
    serializer_class = CollectionSerializer
 
class CollectionDetail(RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
        
    def delete(self, request, pk):
        collection = Collection.objects.annotate(products_count=Count('products')).get(id = pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it include one or more products'})
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)