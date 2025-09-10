from rest_framework import generics, permissions
from django.contrib.auth import get_user_model
from .serializers import UserSerializer


User = get_user_model()


class UserRegisterView(generics.CreateAPIView):
    """Register a new user"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView

class UserDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user
