from django.urls import include, path
from rest_framework import routers
from .views import RegistrationView, activate, LoginView

urlpatterns = [
    path("accounts/activate/<uidb64>/<token>/", activate, name='activate'),
    path("accounts/register/", RegistrationView.as_view(), name='register'),
    path("accounts/login/", LoginView.as_view(), name='login'),
]
