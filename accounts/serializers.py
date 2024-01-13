from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password', 'password2')

    def create(self, validated_data):
        del validated_data['password2']
        return CustomUser.objects.create_user(**validated_data)

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Username must be more than 6 characters long')

        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        if data['email'] == data['username']:
            raise serializers.ValidationError("Email and username can't be same")
        if data['password'] == data['username']:
            raise serializers.ValidationError("Password and username can't be same")
        if data['password'] == data['email']:
            raise serializers.ValidationError("Password and email can't be same")

        return data


class UserLoginSerializer(serializers.Serializer):
    user_identifier = serializers.CharField()
    password = serializers.CharField()


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate(self, data):
        user = self.context['request'].user
        if data['email'] == data['username']:
            raise serializers.ValidationError("Email and username can't be same")
        if user.check_password(data['username']):
            raise serializers.ValidationError("Password and username can't be same")
        if user.check_password(data['email']):
            raise serializers.ValidationError("Password and email can't be same")
        return super().validate(data)

    def validate_username(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Username must be more than 6 characters long')
        return value

    def update(self, instance, validated_data):

        instance.username = validated_data['username']
        instance.email = validated_data['email']

        instance.save()

        return instance


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ["password", "groups", "user_permissions"]