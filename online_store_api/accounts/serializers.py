from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation as validators
from django.core import exceptions
from rest_framework import serializers

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", "username", "email")


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (UserModel.USERNAME_FIELD, "password")

    # Fix issue with password in plain text
    def create(self, validate_data):
        user = super().create(validate_data)

        user.set_password(validate_data["password"])
        user.save()

        return user

    # Invoke password validators
    def validate(self, data):
        user = UserModel(**data)
        password = data.get("password")
        errors = {}
        try:
            validators.validate_password(password, user)
        except exceptions.ValidationError as e:
            errors["password"] = list(e.messages)
        if errors:
            raise serializers.ValidationError(errors)
        return super().validate(data)

    # Remove password from response
    def to_representation(self, instance):
        result = super().to_representation(instance)
        result.pop("password")
        return result


class ChangePasswordSerializer(serializers.Serializer):
    model = UserModel

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
