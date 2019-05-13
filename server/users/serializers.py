from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.models import User

import logging

logging.config.listen()
logger = logging.getLogger(__name__)


class RegistrationSerializer(serializers.ModelSerializer):
    """Registration: Used to register a User"""

    class Meta:
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
        logger.debug('VALIDATED DATA: %s', validated_data)
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],
                                        validated_data['password'])

        return user


class UserSerializer(serializers.ModelSerializer):
    """UserSerializer: Used after successful registration"""

    class Meta:
        model = User
        fields = ('id', 'username', 'email')
