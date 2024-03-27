import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy as gettext_lazy
from django.views.generic import View as BaseView

from moku.forms.user import ProfileForm, UserForm, UserSettingsForm
from moku.images import process_avatar_image
from moku.models.post import Post
from moku.models.user import User
from moku.views.base import FormView, View


class EditProfileView(LoginRequiredMixin, FormView):
    """Allows a user to edit information within their user profile."""

    template_name = "moku/profile/edit.jinja"
    form_class = ProfileForm
    page_title = gettext_lazy("edit profile")

    def form_valid(self, form):
        if "avatar" in form.changed_data and form.instance.avatar.name:
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
    page_title = _("settings")

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

    @property
    def page_title(self):
        return f"@{self.profile.username}"

    @cached_property
    def profile(self):
        return get_object_or_404(User, username=self.kwargs.get("username"))

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "profile": self.profile,
            "posts": self.profile.posts.order_by("-created_at").all(),
        }


class SignupView(FormView):
    """Allows non-authenticated users to create an account on the site."""

    template_name = "moku/signup.jinja"
    form_class = UserForm
    page_title = _("sign up")

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


class UserJSONView(BaseView):
    """
    Renders information about a specific user as JSON, including their latest post.
    """

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=kwargs.get("username"))
        post = (
            Post.objects.prefetch_related("recipe__steps")
            .filter(created_by=user)
            .order_by("-created_at")
            .first()
        )
        if not post:
            post_data = None
        else:
            post_data = {
                "date": {
                    "iso": str(post.created_at),
                    "natural": naturaltime(post.created_at),
                },
                "text": post.get_verb_display()
                % {"user": f"@{post.created_by.username}", "food": post.food},
                "food": post.food,
                "verb": {
                    "id": post.verb,
                    "pattern": post.get_verb_display() % {"user": "$1", "food": "$2"},
                },
                "image": f"{settings.SITE_ROOT_URL}{post.image.url}"
                if post.image
                else None,
                "recipe": [step.instructions for step in post.recipe.steps.all()]
                if post.recipe
                else None,
            }
        user_data = {
            "user": {
                "username": user.username,
                "avatar": f"{settings.SITE_ROOT_URL}{user.avatar.url}"
                if user.avatar
                else None,
                "url": f"{settings.SITE_ROOT_URL}{user.get_absolute_url()}",
                "latest_post": post_data,
            }
        }
        return HttpResponse(json.dumps(user_data), content_type="application/json")
