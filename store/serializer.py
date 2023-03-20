from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title']

class ProductSerialzier(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=255)
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2)
    price_with_tax = serializers.SerializerMethodField(method_name='price_tax')

    # serializing relationships

    # returning id of the collection
    collection = serializers.PrimaryKeyRelatedField(
        queryset = Collection.objects.all()
    )

    # returning title of the collection
    collection = serializers.StringRelatedField()    

    # for adding collection object in response
    collection = CollectionSerializer()

    # for hyperlink 
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name= 'collection-detail'
    )

    def price_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
