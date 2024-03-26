from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from moku.validators import validate_username_length, validate_username_regex


def user_avatar_filename(instance, _):
    """Returns the filename that user avatar images should be saved to."""
    return f"avatars/{instance.username}.webp"


class User(AbstractUser):
    """Represents a single authenticated user on the site."""

    username = models.CharField(
        verbose_name=_("username"),
        max_length=64,
        unique=True,
        db_index=True,
        validators=[validate_username_regex, validate_username_length],
        help_text=_(
            "this is the unique identifier you'll use to log in. it may only contain "
            "letters, numbers, hyphens, dashes and dots."
        ),
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=128,
        unique=True,
        help_text=_(
            "this should be your email address. make sure it's valid and that you have "
            "access to it."
        ),
    )
    email_confirmed_at = models.DateTimeField(blank=True, null=True)
    pronouns = models.CharField(
        verbose_name=_("pronouns"),
        max_length=64,
        blank=True,
        help_text=_("what pronouns should people use when referring to you?"),
    )
    location = models.CharField(
        verbose_name=_("location"),
        max_length=64,
        blank=True,
        help_text=_("where in the world are you?"),
    )
    bio = models.TextField(
        verbose_name=_("about me"),
        blank=True,
        help_text=_("write something about yourself!"),
    )
    avatar = models.ImageField(
        verbose_name=_("avatar"),
        blank=True,
        upload_to=user_avatar_filename,
        help_text=_("a little picture to show up on your profile."),
    )
    last_seen_at = models.DateTimeField(
        verbose_name=_("last seen at"),
        blank=True,
        null=True,
        help_text=_("the last time this user accessed the site."),
    )

    first_name = None
    last_name = None

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("profile", kwargs={"username": self.username})

    @property
    def email_confirmed(self):
        """Whether the user has confirmed their email address."""
        return self.email_confirmed_at is not None


class UserSettings(models.Model):
    """Represents settings for a single user."""

    user = models.OneToOneField(
        "User", related_name="settings", on_delete=models.CASCADE
    )
    language = models.CharField(
        verbose_name=_("language"),
        max_length=16,
        choices=settings.LANGUAGES,
        default="en",
        help_text=_("what language do you want to use moku.blog in?"),
    )
