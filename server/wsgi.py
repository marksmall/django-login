"""
WSGI config for server project.
It exposes the WSGI callable as a module-level variable named ``application``.
For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""
import os

from django.core.wsgi import get_wsgi_application

# configuration = os.getenv('ENVIRONMENT', 'development').title()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
# os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

# from configurations.wsgi import get_wsgi_application

application = get_wsgi_application()
