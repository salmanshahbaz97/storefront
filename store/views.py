from django.shortcuts import get_object_or_404

from .models import Product, Collection
from .serializer import ProductSerialzier, CollectionSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


@api_view()
def collection_detail(request, pk):
    queryset = Collection.objects.get(id = pk)
    serializer = CollectionSerializer(queryset)
    return Response(serializer.data)


@api_view()
def product_list(request):
    queryset = Product.objects.select_related('collection').all().order_by('-id', 'unit_price')
    serializer = ProductSerialzier(queryset, many=True, context={'request': request})
    return Response(serializer.data)
    

@api_view()
def product_detail(request, pk):
    try:
        product = get_object_or_404(Product, pk = pk)
        serializer = ProductSerialzier(product)
        return Response(serializer.data)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)