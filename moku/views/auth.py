from django.contrib import messages
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from moku.views.base import View


class LoginView(View, BaseLoginView):
    template_name = "moku/login.jinja"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            messages.success(
                self.request,
                _("welcome back, %(username)s!")
                % {"username": self.request.user.username},
            )
        return self.request.GET.get("next", reverse_lazy("feed"))


class LogoutView(BaseLogoutView):
    next_page = "feed"
