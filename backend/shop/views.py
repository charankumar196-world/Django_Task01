from rest_framework import generics, permissions
from users.serializers import UserSerializer

from .models import Product, Cart, CartItem, Order
from rest_framework import generics, permissions
from .models import Category, Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    CartSerializer,
    CartItemSerializer,
    OrderSerializer,
    OrderItemSerializer,
)
from users.serializers import UserSerializer   # ✅ correct import

# --------------------
# Products
# --------------------
class ProductListView(generics.ListCreateAPIView):
    """List all products or create a new one."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """Retrieve, update, or delete a single product."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# --------------------
# Cart
# --------------------
class CartView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the current user's cart."""
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, active=True)
        return cart


class CartItemAddView(generics.CreateAPIView):
    """Add a product to the cart."""
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        cart, _ = Cart.objects.get_or_create(user=self.request.user, active=True)
        serializer.save(cart=cart)


# --------------------
# Orders
# --------------------
class OrderListView(generics.ListCreateAPIView):
    """List all orders for the user, or create a new one."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        cart = Cart.objects.filter(user=self.request.user, active=True).first()
        if cart:
            total = sum(item.product.price * item.quantity for item in cart.items.all())
            order = serializer.save(user=self.request.user, total=total, paid=False)
            for item in cart.items.all():
                order.items.create(
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
            cart.active = False
            cart.save()


class OrderDetailView(generics.RetrieveAPIView):
    """Retrieve details of a single order."""
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer
from users.views import UserRegisterView, UserDetailView


User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    """Register a new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveAPIView):
    """Get details of the logged-in user"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
