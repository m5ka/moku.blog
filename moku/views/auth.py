from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from moku.forms.auth import AuthenticationForm
from moku.views.base import View


class LoginView(View, BaseLoginView):
    """Allows users to log in by username and password."""

    template_name = "moku/login.jinja"
    form_class = AuthenticationForm
    page_title = "log in"
    redirect_authenticated_user = True

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(
                self.request,
                _("welcome back, %(username)s!")
                % {"username": self.request.user.username},
            )
        return reverse_lazy("feed")


class LogoutView(BaseLogoutView):
    """Logs the user out and redirect them to the feed."""

    next_page = "feed"
