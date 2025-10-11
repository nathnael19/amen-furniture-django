from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def get_cart(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart

    def list(self, request):
        """GET /api/v1/cart/ - View current user's cart"""
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=["post"], url_path="add")
    def add_item(self, request):
        """POST /api/v1/cart/add/ - Add product to cart"""
        cart = self.get_cart(request)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"detail": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity},
        )

        if not created:
            item.quantity += quantity
            item.save()

        return Response(CartItemSerializer(item).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["patch"], url_path="update")
    def update_item(self, request, pk=None):
        """PATCH /api/v1/cart/{item_id}/update/ - Update quantity"""
        try:
            item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CartItemSerializer(item, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=True, methods=["delete"], url_path="remove")
    def remove_item(self, request, pk=None):
        """DELETE /api/v1/cart/{item_id}/remove/ - Remove item"""
        try:
            item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({"detail": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
