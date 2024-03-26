from pathlib import Path

import environ
from django.utils.translation import gettext_lazy as _

# Initial environment
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent.parent
env.read_env(BASE_DIR / ".env")

# Debug
DEBUG = env.bool("DEBUG", default=False)

# Secret key
SECRET_KEY = env.str("SECRET_KEY", default="insecure-keyboard-cat-abcd1234")

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_jinja",
    "django_jinja.contrib._humanize",
    "django_recaptcha",
    "moku",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "moku.middleware.MokuLanguageMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Debug toolbar
# https://django-debug-toolbar.readthedocs.io/en/latest/
if DEBUG and env.bool("DEBUG_TOOLBAR", default=True):
    try:
        import debug_toolbar  # noqa: F401

        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
        DEBUG_TOOLBAR = True
    except ImportError:
        DEBUG_TOOLBAR = False
else:
    DEBUG_TOOLBAR = False

ROOT_URLCONF = "moku.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
            "filters": {"unemoji": "moku.filters.unemoji"},
            "policies": {"ext.i18n.trimmed": True},
        },
    },
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    },
]

WSGI_APPLICATION = "moku.config.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    "default": env.db(
        "DATABASE_URL", engine="postgres", default="postgres://localhost:5432/moku"
    )
}

# Authentication models
# https://docs.djangoproject.com/en/5.0/topics/auth/customizing/
AUTH_USER_MODEL = "moku.User"
LOGIN_URL = "login"

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        )
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internal IP addresses
# https://docs.djangoproject.com/en/5.0/ref/settings/
INTERNAL_IPS = ["localhost", "127.0.0.1"]

# Allowed hosts
# https://docs.djangoproject.com/en/5.0/ref/settings/#allowed-hosts
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", cast=str, default=[])

# CSRF trusted origins
# https://docs.djangoproject.com/en/5.0/ref/settings/#csrf-trusted-origins
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", cast=str, default=[])

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = "en-gb"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# Available languages
# https://docs.djangoproject.com/en/5.0/ref/settings/#languages
LANGUAGES = [
    ("en", _("english")),
    ("lio", _("lami lioa")),
    ("tok", _("toki pona")),
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = env.str("STATIC_URL", default="static/")
STATIC_ROOT = BASE_DIR / "moku/static"

# User-uploaded content
# https://docs.djangoproject.com/en/5.0/ref/settings/#media-root
MEDIA_URL = env.str("MEDIA_URL", default="media/")
MEDIA_ROOT = BASE_DIR / "media"

# Email settings
# https://docs.djangoproject.com/en/5.0/topics/email/
EMAIL_FROM = env.str("EMAIL_FROM", default='"Sender" <sender@example.com>')
EMAIL_HOST = env.str("EMAIL_HOST", default="localhost")
EMAIL_PORT = env.int("EMAIL_PORT", default=25)
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=False)
EMAIL_USE_SSL = env.bool("EMAIL_USE_SSL", default=False)
EMAIL_TIMEOUT = env.int("EMAIL_TIMEOUT", default=3)

# Username length
USERNAME_MIN_LENGTH = 3
USERNAME_MAX_LENGTH = 24

# URL configuration
SITE_ROOT_URL = env.str("SITE_ROOT_URL", default="https://moku.blog")

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Recaptcha settings
# https://pypi.org/project/django-recaptcha/#installation
if DEBUG:
    SILENCED_SYSTEM_CHECKS = ["django_recaptcha.recaptcha_test_key_error"]
else:
    RECAPTCHA_PUBLIC_KEY = env.str("RECAPTCHA_PUBLIC_KEY")
    RECAPTCHA_PRIVATE_KEY = env.str("RECAPTCHA_PRIVATE_KEY")
