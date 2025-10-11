from rest_framework import serializers
from .models import Product, Category,ProductImage,ProductVariant
from users.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['image', 'is_main','alt_text']


class ProducVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['material','color']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProducVariantSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
