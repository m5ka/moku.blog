import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "moku.config.settings")

application = get_wsgi_application()
"""
WSGI application for moku.blog.
More information: https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""
