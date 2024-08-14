from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.Serializer):
    
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)

    def validate(self, data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('Username already exists')
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
           
            email=validated_data['email'],
            username=validated_data['username'].lower(),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    
    def validate(self, data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('User Account Not Found')
        
        return data
    
    
    def get_jwt_token(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            return {'message': 'Invalid Credentials', 'data': {}}
        
        refresh = RefreshToken.for_user(user)
        
        return {'message': 'Login Successful', 'data': {'token': {'refresh': str(refresh), 'access': str(refresh.access_token)}}}
