""" User Account related serializers """

import logging

from django.contrib.auth import authenticate
# from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User
from rest_framework import serializers

logging.config.listen()
LOGGER = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    """Registration: Used to register a User"""

    class Meta(object):
        """ Meta: """
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': True,
                'min_length': 8,
                'max_length': 32,
            },
            'username': {
                'required': True,
                'min_length': 8,
                'max_length': 32,
            },
            'email': {
                'required': True,
            },
        }

    def create(self, validated_data):
        """ Create a new User Account """
        LOGGER.debug('VALIDATED DATA: %s', validated_data)
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])

        return user


class LoginSerializer(serializers.Serializer):
    """ LoginSerializer: Used to login """
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        """ Validate user has an account and that old password matches """
        LOGGER.debug(f"Validating {data}")
        user = authenticate(**data)
        if user and user.is_active:
            return user

        raise serializers.ValidationError(
            "Unable to login with provided credentials")


# class ChangePasswordSerializer(serializers.Serializer):
#     """ LoginSerializer: Used to login """
#     username = serializers.CharField()
#     old_password = serializers.CharField()
#     new_password = serializers.CharField()

#     def validate(self, data):
#         """ Validate user has an account and that credentials match """
#         user = authenticate(**data)
#         if user and user.is_active:
#             return user

#         raise serializers.ValidationError(
#             "Unable to login with provided credentials")


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer: Used after successful registration"""

    class Meta(object):
        """ Meta class for UserSerializer """
        model = User
        fields = ('id', 'username', 'email', 'profile')
