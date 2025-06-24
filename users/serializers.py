from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer
from users.models import User
from rest_framework.exceptions import ValidationError


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['password', "user_permissions", 'groups']


class UserLoginSerializer(Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name',
                  'date_birthday', 'gender', 'height', 'weight']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value


class ChangePasswordSerializer(Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise ValidationError("Current password is incorrect")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise ValidationError("New passwords don't match")

        if data['old_password'] == data['new_password']:
            raise ValidationError("New password must be different from old")

        return data
