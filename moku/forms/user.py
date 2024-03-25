from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from django_recaptcha.fields import ReCaptchaField

from moku.models.user import User


class UserForm(UserCreationForm):
    password1 = forms.CharField(
        label=_("password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=_("make a secure password that you've never used before!"),
    )
    password2 = forms.CharField(
        label=_("password (again)"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=_("just type the password again to confirm."),
    )
    captcha = ReCaptchaField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")
        labels = {
            "username": _("username"),
            "email": _("email address"),
        }
        help_texts = {
            "username": User._meta.get_field("username").help_text,
            "email": User._meta.get_field("email").help_text,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["captcha"].error_messages = {"required": _("make sure you've ticked the captcha.")}


class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("pronouns", "location", "bio")
        labels = {
            "pronouns": _("pronouns"),
            "location": _("location"),
            "bio": _("about me"),
        }
