"""
WSGI config for clubdata project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'clubdata.settings')

application = get_wsgi_application()