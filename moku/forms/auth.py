from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.utils.translation import gettext_lazy as _


class AuthenticationForm(BaseAuthenticationForm):
    error_messages = {
        "invalid_login": _("sorry! that username and password didn't work."),
        "inactive": _("your account has been deactivated."),
    }

    def clean_username(self):
        return self.cleaned_data.get("username").lower()
