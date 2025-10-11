from rest_framework.permissions import BasePermission
from rest_framework import generics,permissions
from rest_framework import filters
from .serializers import RegisterSerializer,UserSerializer,ViewUserSerializer
from .models import User


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class Profile(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    

class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class ViewUserView(generics.ListAPIView):
    
    serializer_class = ViewUserSerializer
    permission_classes = [IsSuperUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username','email','first_name','last_name']
    def get_queryset(self):
        return User.objects.exclude(id=self.request.user.id)
