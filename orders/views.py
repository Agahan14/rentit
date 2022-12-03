from django.shortcuts import get_object_or_404
from rest_framework import (
    viewsets,
    permissions,
    status,
)
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework.exceptions import (
    NotAcceptable,
    ValidationError,
    PermissionDenied,
)
from .serializers import (
    CartSerializer,
    CartMiniSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderMiniSerializer,
    CartItemUpdateSerializer,
)
from .models import (
    Cart,
    CartItem,
    Order,
)
from products.models import Product


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    lookup_field = "user_id"

    def get_serializer_class(self):
        if self.action == 'list':
            return CartSerializer
        return CartMiniSerializer
    # http_method_names = ['GET', 'POST']


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    queryset = CartItem.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        product = get_object_or_404(Product, pk=request.data["product"])
        current_item = CartItem.objects.filter(cart=cart, product=product)
        cart.count += 1
        cart.save()

        if user == product.user:
            raise PermissionDenied("This Is Your Product")

        if current_item.count() > 0:
            raise NotAcceptable("You already have this item in your shopping cart")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please Enter Your Quantity")

        if quantity > product.quantity:
            raise NotAcceptable("You order quantity more than the seller have")

        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        serializer = self.get_serializer(cart_item)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        cart_item = self.get_object()
        product = get_object_or_404(Product, pk=request.data["product"])

        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")

        try:
            quantity = int(request.data["quantity"])
        except Exception as e:
            raise ValidationError("Please, input validd quantity")

        if quantity > product.quantity:
            raise NotAcceptable("Your order quantity more than the seller have")

        serializer = CartItemUpdateSerializer(cart_item, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        cart_item = self.get_object()
        if cart_item.cart.user != request.user:
            raise PermissionDenied("Sorry this cart not belong to you")
        cart_item.delete()

        return Response(
            {"detail": "your item has been deleted."},
            status=status.HTTP_204_NO_CONTENT,
        )


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.user
        cart = get_object_or_404(Cart, user=user)

        order = Order(cart=cart, user=user)
        order.save()
        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return OrderSerializer
        return OrderMiniSerializer

