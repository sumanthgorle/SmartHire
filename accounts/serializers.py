from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(
        write_only=True
    )

    role = serializers.CharField(
        write_only=True
    )

    phone = serializers.CharField(
        write_only=True
    )

    bio = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User

        fields = [
            'username',
            'password',
            'role',
            'phone',
            'bio'
        ]

    def create(self, validated_data):

        role = validated_data.pop('role')
        phone = validated_data.pop('phone')
        bio = validated_data.pop('bio')

        user = User.objects.create_user(
            **validated_data
        )

        Profile.objects.create(
            user=user,
            role=role,
            phone=phone,
            bio=bio
        )

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )