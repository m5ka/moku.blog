import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moku.config.settings")

application = get_asgi_application()
"""
ASGI application for moku.blog.
More information: https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""
