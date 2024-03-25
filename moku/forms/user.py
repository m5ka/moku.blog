from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField

from moku.models.user import User


class UserForm(UserCreationForm):
    captcha = ReCaptchaField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")
        labels = {
            "username": _("username"),
            "email": _("email address"),
            "password1": _("password"),
            "password2": _("password (again)"),
        }
        help_texts = {
            "username": User._meta.get_field("username").help_text,
            "email": User._meta.get_field("email").help_text,
            "password1": _("make a secure password that you've never used before!"),
            "password2": _("just type the password again to confirm"),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha"].error_messages = {"required": _("make sure you've ticked the captcha.")}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("avatar", "pronouns", "location", "bio")
        labels = {
            "avatar": _("avatar"),
            "pronouns": _("pronouns"),
            "location": _("location"),
            "bio": _("about me"),
        }
