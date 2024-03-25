from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from moku.validators import validate_username_regex, validate_username_length


class User(AbstractUser):
    username = models.CharField(
        verbose_name=_("username"),
        max_length=64,
        unique=True,
        db_index=True,
        validators=[validate_username_regex, validate_username_length],
        help_text=_(
            "this is the unique identifier you'll use to log in. it may only contain "
            "letters, numbers, hyphens, dashes and dots."
        )
    )
    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=128,
        unique=True,
        help_text=_(
            "this should be your email address. make sure it's valid and that you have "
            "access to it."
        )
    )
    email_confirmed_at = models.DateTimeField(
        blank=True,
        null=True,
    )
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
        return self.email_confirmed_at is not None
