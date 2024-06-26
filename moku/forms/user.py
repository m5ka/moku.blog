from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _
from django_recaptcha.fields import ReCaptchaField

from moku.models.user import User


class UserForm(UserCreationForm):
    """Form for creating a new user account on the site."""

    captcha = ReCaptchaField(required=True)
    check = forms.BooleanField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {"username": _("username"), "email": _("email address")}
        help_texts = {
            "username": User._meta.get_field("username").help_text,
            "email": User._meta.get_field("email").help_text,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha"].error_messages = {
            "required": _("make sure you've ticked the captcha.")
        }
        self.fields["check"].error_messages = {
            "required": _("you must agree to the terms of use and privacy policy.")
        }


class UserSettingsForm(forms.ModelForm):
    """Form for creating or updating user settings."""

    class Meta:
        model = User
        fields = ("language",)
        labels = {"language": _("language")}


class ProfileForm(forms.ModelForm):
    """Form for updating user profile information."""

    class Meta:
        model = User
        fields = ("avatar", "pronouns", "location", "bio")
        labels = {
            "avatar": _("avatar"),
            "pronouns": _("pronouns"),
            "location": _("location"),
            "bio": _("about me"),
        }
