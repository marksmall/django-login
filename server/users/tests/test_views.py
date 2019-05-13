import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)


@pytest.mark.django_db
class TestRegistrationView:
    def test_successful_registration(self, client):
        user = {
            "username": "testusername1",
            "password": "password",
            "email": "email@test.com"
        }

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_201_CREATED
        test_user = User.objects.get(username=user["username"],
                                     email=user["email"])
        logger.debug('TEST USER: %s', test_user)
        assert test_user

    def test_missing_password(self, client):
        user = {"username": "testusername1", "email": "email@test.com"}

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_missing_username(self, client):
        user = {"password": "password", "email": "email@test.com"}

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplicate_username(self, client):
        user = {
            "username": "testusername1",
            "password": "password",
            "email": "email@test.com"
        }

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        response = client.post(url, data=user, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_missing_email(self, client):
        user = {"username": "testusername1", "password": "password"}

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_to_short(self, client):
        user = {
            "username": "testusername1",
            "password": "pass",
            "email": "email@test.com"
        }

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_password_to_long(self, client):
        user = {
            "username": "testusername1",
            "password": "passwordpasswordpasswordpasswordpasswordpassword",
            "email": "email@test.com"
        }

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_username_to_short(self, client):
        user = {
            "username": "t",
            "password": "password",
            "email": "email@test.com"
        }

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_username_to_long(self, client):
        user = {
            "username": "testusername1testusername1testusername1",
            "password": "password",
            "email": "email@test.com"
        }

        url = reverse('register')
        response = client.post(url, data=user, format="json")
        logger.debug('RESPONSE: %s', response)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
