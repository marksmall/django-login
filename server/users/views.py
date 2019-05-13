from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.forms.models import model_to_dict

from .serializers import RegistrationSerializer, UserSerializer

from .tokens import account_activation_token

import logging, json

logging.config.listen()
logger = logging.getLogger(__name__)


class RegistrationView(GenericAPIView):
    """RegistrationView"""
    serializer_class = RegistrationSerializer
    permission_classes = (AllowAny, )

    def post(self, request, *args, **kwargs):
        logger.info('Registration Data: %s', request.data)
        serializer = self.get_serializer(data=request.data)

        if (serializer.is_valid()):
            user = serializer.save()
            user.is_active = False
            user.save()
            logger.debug('USER: %s', user)

            site = get_current_site(request)
            subject = 'Activate Your Account'
            token = account_activation_token.make_token(user)
            message = render_to_string(
                'account-activation-email.html', {
                    'user': user,
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(
                        user.pk)).decode(),
                    'token': token,
                })
            logger.info('Emailing activation token [%s] to user [%s]', message,
                        user)
            user.email_user(subject, message)

            return Response(UserSerializer(
                user, context=self.get_serializer_context()).data,
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([AllowAny])
def activate(request, uidb64, token):
    logger.info('Activation Data: %s', request.data)
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        logger.debug('DECODED PK: %s', uid)
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        logger.error('Cannot find user  for uid [%s], with token [%s]',
                     uidb64,
                     token,
                     exc_info=True)
        user = None
    logger.debug('USER BEING ACTIVATED: %s', user)

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
    logger.info('User [%s] activated', user)

    # login(request, user)

    serializer = UserSerializer(user)
    if (serializer.is_valid):
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        logger.error('Error Activating User [%s], with Data [%s]', user,
                     request.data)
        return Response({"error": "User is not valid"},
                        status=status.HTTP_400_BAD_REQUEST)
