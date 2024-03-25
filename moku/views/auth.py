from django.contrib.auth.views import LoginView as BaseLoginView, LogoutView as BaseLogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoginView(BaseLoginView):
    template_name = "moku/login.jinja"

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return self.request.GET.get("next", reverse_lazy("feed"))


class LogoutView(BaseLogoutView):
    next_page = "feed"
