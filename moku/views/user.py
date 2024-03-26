from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from moku.forms.user import ProfileForm, UserForm, UserSettingsForm
from moku.images import process_avatar_image
from moku.models.user import User
from moku.views.base import FormView, View


class EditProfileView(LoginRequiredMixin, FormView):
    """Allows a user to edit information within their user profile."""

    template_name = "moku/profile/edit.jinja"
    form_class = ProfileForm

    def form_valid(self, form):
        if "avatar" in form.changed_data and form.instance.avatar is not None:
            form.instance.avatar = process_avatar_image(form.instance.avatar)
        form.save()
        messages.success(self.request, _("profile updated successfully!"))
        return redirect("profile", username=form.instance.username)

    def get_form(self):
        return self.form_class(instance=self.request.user, **self.get_form_kwargs())


class EditSettingsView(LoginRequiredMixin, FormView):
    """Allows a user to edit information within their user settings."""

    template_name = "moku/settings.jinja"
    form_class = UserSettingsForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        try:
            form.save()
        except IntegrityError:
            messages.error(
                self.request, _("uh oh. i think something went a little bit oopsie.")
            )
            return self.form_invalid(form)
        messages.success(self.request, _("settings updated!"))
        return redirect("settings")

    def get_form(self):
        if hasattr(self.request.user, "settings"):
            return self.form_class(
                instance=self.request.user.settings, **self.get_form_kwargs()
            )
        return super().get_form()


class ProfileView(View):
    """Shows a user's profile along with a list of their recent posts."""

    template_name = "moku/profile/show.jinja"

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.kwargs.get("username"))
        return {
            **super().get_context_data(**kwargs),
            "profile": user,
            "posts": user.posts.order_by("-created_at").all(),
        }


class SignupView(FormView):
    """Allows non-authenticated users to create an account on the site."""

    template_name = "moku/signup.jinja"
    form_class = UserForm

    def form_valid(self, form):
        form.instance.username = form.instance.username.lower()
        try:
            form.save()
        except IntegrityError:
            messages.error(
                self.request, _("sorry! someone else got to that username first.")
            )
            return self.form_invalid(form)
        messages.success(
            self.request, _("that's it! just log in, and you're ready to go.")
        )
        return redirect("login")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("feed")
        return super().get(request, *args, **kwargs)
