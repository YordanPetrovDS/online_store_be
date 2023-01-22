from django.contrib.auth import get_user_model
from django.contrib.auth import password_validation as validators
from django.core import exceptions
from rest_framework import serializers
from rest_framework.authtoken.models import Token

UserModel = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ("id", UserModel.USERNAME_FIELD, "password", "email")

    # Create user
    def create(self, validate_data):
        user = UserModel.objects.create_user(
            username=validate_data["username"],
            password=validate_data["password"],
            email=validate_data["email"],
        )
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
        token = Token.objects.get(user=instance)
        result["token"] = token.key
        return result
