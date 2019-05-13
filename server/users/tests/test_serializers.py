import pytest

from server.users.serializers import RegistrationSerializer

import logging

logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestRegistrationSerializer:
    def test_successful_serialization(self):
        user = {
            "username": "testusername1",
            "password": "password",
            "email": "email@test.com"
        }

        serializer = RegistrationSerializer(user)

        assert serializer.is_valid
        assert serializer.data["username"] == "testusername1"
        assert serializer.data["email"] == "email@test.com"
        assert "password" not in serializer.data

    def test_missing_username(self):
        user = {
            "username": "",
            "password": "password",
            "email": "email@test.com"
        }

        serializer = RegistrationSerializer(data=user)
        assert serializer.is_valid() == False
