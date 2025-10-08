from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Cart,CartItem
from .serializers import CartSerializer,CartItemSerializer


class CartViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_cart(self,request):
        user = request.user if request.user.is_authenticated else None
        cart,_ = Cart.objects.get_or_create(user=user)
        return cart
    
    def list(self,request):
        cart = self.get_cart(request)
        serializer = CartSerializer(cart)
        return Response(serializer.data)
    
    def add_item(self,request):
        cart = self.get_cart(request)
        serializer = CartItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']

        item,created  = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={
                "quantity":quantity
            }
        )
        if not created:
            item.quantity +=quantity
            item.save()

        return Response(CartItemSerializer(item).data,status=status.HTTP_201_CREATED)
    
    def update_item(self,request,pk=None):
        try:
            item = CartItem.objects.get(pk=pk, cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response(
                {
                    "detail":"Item not Found!!"
                },status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = CartItemSerializer(item,data=request.data,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def remove_item(self,request,pk=None):
        try:
            item = CartItem.objects.get(pk=pk,cart__user=request.user)
        except CartItem.DoesNotExist:
            return Response({
                "detail":"Item not Found!"
            },
            status=status.HTTP_404_NOT_FOUND
            )
        
        item.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

