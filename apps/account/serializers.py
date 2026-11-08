from rest_framework import serializers

from .models import (
    User,
    # Profile
)


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('full_name', 'email','profile_pic','dob', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        try:
            user = User.objects.create_user(**validated_data)
        except Exception as e:
            raise serializers.ValidationError(e)
        return user

class DeactivateAccountSerializer(serializers.Serializer):
    confirm = serializers.BooleanField()

class DeleteAccountSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)

from rest_framework import serializers
from .models import User


class UserProfileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("full_name", "phone", "profile_pic")

    def validate_phone(self, value):
        if value and len(value) < 7:
            raise serializers.ValidationError("Invalid phone number")
        return value
from rest_framework import serializers


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match"}
            )
        return data
