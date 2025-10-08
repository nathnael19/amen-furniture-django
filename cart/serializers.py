from rest_framework import serializers
from .models import CartItem ,Cart
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.UUIDField(write_only=True)
    
    subtotal = serializers.DecimalField(max_digits=10,decimal_places=2,read_only=True)

    class Meta:
        model = CartItem
        fields = ['id','product','product_id','quantity','subtotal']


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)
    total = serializers.DecimalField(decimal_places=2,max_digits=10,read_only=True)

    class Meta:
        model = Cart
        fields = ['id','user','items','total']
        read_only_fields = ['user']        