from training_tracker.service import BaseService
from users.serializers import UserLoginSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import authenticate
from django.http.response import HttpResponseBadRequest
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status

class UserService(BaseService):

    def authenticate_user(self, data):
        serializer = UserLoginSerializer(data=data)
        if not serializer.is_valid():
            return {'error': 'Invalid data', 'details': serializer.errors}

        user = authenticate(
            username=serializer.initial_data.get('username'),
            password=serializer.initial_data.get('password')
        )

        if not user:
            return {'error': 'Invalid credentials'}

        if not user.is_active:
            return {'error': 'User account is disable'}

        token, _ = Token.objects.get_or_create(user=user)
        return {'token': token}

    def register_user(self, data):
        serializer = RegisterSerializer(data=data)
        if not serializer.is_valid():
            return {'error': 'Validation error', 'details': serializer.errors}
        try:
            user = serializer.save()
            user.is_active = True
            user.save()

            Token.objects.create(user=user)

            return UserSerializer(user).data
        except Exception as e:
            return {'error': str(e)}


