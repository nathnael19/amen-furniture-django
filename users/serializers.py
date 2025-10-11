from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User,Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"

class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer(read_only=True)
    class Meta:
        model = User
        fields = "__all__"

    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone']
        )

        return user
    

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username','email','phone','password','first_name','last_name']

    
    def create(self,validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
        )

class ViewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email,password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password")
        data['user'] = user
        return data