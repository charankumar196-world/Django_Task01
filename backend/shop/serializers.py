# shop/serializers.py
# --------------------
# Serializers for:
# - Category
# - Product
# - Cart & CartItem
# - Order & OrderItem
#
# Serializers convert Django models into JSON (for API responses)
# and validate incoming JSON (for API requests).

from rest_framework import serializers
from .models import Category, Product, Cart, CartItem, Order, OrderItem


# --------------------
# Category
# --------------------
class CategorySerializer(serializers.ModelSerializer):
    """Serialize product categories (id + name)."""
    class Meta:
        model = Category
        fields = ['id', 'name']


# --------------------
# Product
# --------------------
class ProductSerializer(serializers.ModelSerializer):
    """Serialize product details including owner and category."""
    owner = serializers.ReadOnlyField(source='owner.id')  # only show owner id

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'description',
            'price',
            'owner',
            'category',
            'image',
            'created_at',
            'updated_at',
        ]


# --------------------
# Cart & CartItem
# --------------------
class CartItemSerializer(serializers.ModelSerializer):
    """Serialize individual cart items."""
    product_detail = ProductSerializer(source='product', read_only=True)  # nested product info

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_detail', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    """Serialize the cart with all nested items."""
    items = CartItemSerializer(many=True, read_only=True)  # nested items list

    class Meta:
        model = Cart
        fields = ['id', 'user', 'active', 'items']
        read_only_fields = ['user']  # user auto-set from request


# --------------------
# Order & OrderItem
# --------------------
class OrderItemSerializer(serializers.ModelSerializer):
    """Serialize each product inside an order."""
    product_detail = ProductSerializer(source='product', read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_detail', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    """Serialize the whole order with nested items."""
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'paid', 'created_at', 'items']
        read_only_fields = ['user', 'total', 'paid']
