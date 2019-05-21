""" User Account Views """

import logging

# from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .serializers import RegistrationSerializer, UserSerializer, LoginSerializer
from .tokens import account_activation_token

logging.config.listen()
LOGGER = logging.getLogger(__name__)


class RegistrationView(GenericAPIView):
    """RegistrationView"""
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """ Receive registration request """
        LOGGER.info('Registration Data: %s', request.data)
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user.is_active = False
            user.save()
            LOGGER.debug('USER: %s', user)

            site = get_current_site(request)
            subject = 'Activate Your Account'
            token = account_activation_token.make_token(user)
            message = render_to_string(
                'account-activation-email.html', {
                    'user': user,
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                })
            LOGGER.info('Emailing activation token [%s] to user [%s]', message,
                        user)
            user.email_user(subject, message)

            return Response(UserSerializer(user).data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    LOGGER.info('Activation Data: %s', request.data)
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        LOGGER.debug('DECODED PK: %s', uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        LOGGER.error('Cannot find user  for uid [%s], with token [%s]',
                     uidb64,
                     token,
                     exc_info=True)
        user = None
    LOGGER.debug('USER BEING ACTIVATED: %s', user)

    if user is None:
        return Response({"error": "No user to activate"},
                        status=status.HTTP_400_BAD_REQUEST)
    if user.is_active == True:
        return Response({"error": "User already activated"},
                        status=status.HTTP_400_BAD_REQUEST)
    if account_activation_token.check_token(user, token) == False:
        return Response({"error": "Token failed verification"},
                        status=status.HTTP_400_BAD_REQUEST)

    user.is_active = True
    user.profile.email_confirmed = True
    user.save()
    LOGGER.info('User [%s] activated', user)

    # login(request, user)

    serializer = UserSerializer(user)
    if (serializer.is_valid):
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        LOGGER.error('Error Activating User [%s], with Data [%s]', user,
                     request.data)
        return Response({"error": "User is not valid"},
                        status=status.HTTP_400_BAD_REQUEST)


class LoginView(GenericAPIView):
    """ View enabling users to login to their account """
    serializer_class = LoginSerializer
    permission_classes = (AllowAny, )

    def post(self, request):
        """ Handle login request """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data
            return Response(UserSerializer(user).data, status.HTTP_200_OK)
        else:
            LOGGER.error(f"{request.data} not valid: {serializer.errors}")
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
