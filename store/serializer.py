from decimal import Decimal
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem


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


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'name', 'description', 'date']
    
    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    

class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']
    

class CartItemSerializer(serializers.ModelSerializer):
    product_serializer = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'product_serializer', 'product', 'quantity', 'cart', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_price = serializers.SerializerMethodField(method_name='get_cart_price')
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_cart_price']

    def get_cart_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])