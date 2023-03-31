from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'inventory','unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(method_name='price_tax')

    # serializing relationships

    # # returning id of the collection
    # collection = serializers.PrimaryKeyRelatedField(
    #     queryset = Collection.objects.all()
    # )

    # # returning title of the collection
    # collection = serializers.StringRelatedField()    

    # # for adding collection object in response
    # collection = CollectionSerializer()

    # for hyperlink 
    collection = serializers.HyperlinkedRelatedField(
        queryset = Collection.objects.all(),
        view_name= 'collection-detail'
    )

    def price_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
