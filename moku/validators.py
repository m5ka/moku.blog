import re

from django.conf import settings
from django.core.validators import RegexValidator, ValidationError
from django.utils.translation import gettext_lazy as _
from emoji import is_emoji


def validate_emoji(value):
    """Validates that a given string is a single emoji."""
    if not is_emoji(value):
        raise ValidationError(_("Must be an emoji."))


validate_username_regex = RegexValidator(
    re.compile(r"^[a-zA-Z0-9-_.]+\Z"),
    _("Username may only contain letters, numbers, hyphens, underscores and dots."),
    "invalid",
)
"""Validates that a given string is a valid username."""


def validate_username_length(value):
    """Validates the length of a given username string according to Django settings."""
    if (
        len(value) < settings.USERNAME_MIN_LENGTH
        or len(value) > settings.USERNAME_MAX_LENGTH
    ):
        raise ValidationError(
            _("Username must be between %(min_length)d and %(max_length)d characters.")
            % {
                "min_length": settings.USERNAME_MIN_LENGTH,
                "max_length": settings.USERNAME_MAX_LENGTH,
            }
        )
