from rest_framework import serializers
from decimal import Decimal
from .models import Cart, CartItem, Order
from products.models import Product


class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "title",
            "seller",
            "quantity",
            "price",
            "image",
        ]


class CartItemSerializer(serializers.ModelSerializer):
    price = serializers.FloatField(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'quantity',
            'price',
            'product',
            'cart',
        ]


class CartItemMiniSerializer(serializers.ModelSerializer):
    product = CartProductSerializer(required=False)

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = [
            'id',
            'user',
            'total_price',
            'created_date',
            'is_order',
        ]

    def get_total_price(self, obj):
        cart_id = obj.id
        cart_items = CartItem.objects.filter(cart=cart_id)
        price = 0
        for item in cart_items:
            price += Decimal(item.product.price) * Decimal(item.quantity)
        return price


class OrderSerializer(serializers.ModelSerializer):
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'user',
            'cart',
            'order_date',
            'total_price',
        ]

    def get_total_price(self, obj):
        obj.total_price = obj.cart.cart_price
        obj.save()
        return obj.total_price
