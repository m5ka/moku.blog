from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from moku.constants import EMOJI_CATEGORIES, Verbs
from moku.forms.post import DeletePostForm, PostForm
from moku.images import process_post_image
from moku.models.post import Post
from moku.models.recipe import Recipe
from moku.views.base import FormView


def _get_verbs(username):
    return (
        (verb[0], verb[1] % {"user": f"@{username}", "food": "..."})
        for verb in Verbs.CHOICES
    )


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """Allows users to delete their previous posts."""

    template_name = "moku/delete.jinja"
    form_class = DeletePostForm

    def form_valid(self, form):
        self.post_object.delete()
        messages.success(self.request, _("post deleted successfully!"))
        return redirect("feed")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "item": _("%(post_text)s from %(time_ago)s")
            % {
                "post_text": self.post_object.plain_text,
                "time_ago": naturaltime(self.post_object.created_at),
            },
            "back_url": reverse("post.edit", kwargs={"uuid": self.post_object.uuid}),
        }

    @cached_property
    def post_object(self):
        return get_object_or_404(Post, uuid=self.kwargs.get("uuid"))

    def test_func(self):
        return self.request.user.id == self.post_object.created_by.id


class EditPostview(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """Allows users to edit their previous posts."""

    template_name = "moku/post/edit.jinja"
    form_class = PostForm

    def form_valid(self, form):
        if (
            form.instance.recipe
            and form.instance.recipe.created_by.id != self.request.user.id
        ):
            messages.error(
                self.request, _("you can't add someone else's recipe to your post!")
            )
            return self.form_invalid(form)
        if "image" in form.changed_data and form.instance.image.name:
            form.instance.image = process_post_image(form.instance.image)
        form.save()
        messages.success(self.request, _("your post was updated!"))
        return redirect("feed")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "post": self.post_object,
            "verbs": _get_verbs(self.request.user.username),
            "emoji": EMOJI_CATEGORIES,
        }

    def get_form(self):
        form = self.form_class(instance=self.post_object, **self.get_form_kwargs())
        form.fields["recipe"].queryset = Recipe.objects.filter(
            created_by=self.request.user
        )
        return form

    @cached_property
    def post_object(self):
        return get_object_or_404(Post, uuid=self.kwargs.get("uuid"))

    def test_func(self):
        return self.post_object.created_by.id == self.request.user.id


class FeedView(FormView):
    """Allows users to see recent posts and create a new post."""

    template_name = "moku/post/index.jinja"
    form_class = PostForm

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        if (
            form.instance.recipe
            and form.instance.recipe.created_by.id != self.request.user.id
        ):
            messages.error(
                self.request, _("you can't add someone else's recipe to your post!")
            )
            return redirect("feed")
        form.instance.created_by = self.request.user
        if "image" in form.changed_data and form.instance.image.name:
            form.instance.image = process_post_image(form.instance.image)
        form.save()
        messages.success(self.request, _("your post was made!"))
        return redirect("feed")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "posts": Post.objects.all()[:128],
        }
        if self.request.user.is_authenticated:
            return self.get_authenticated_context_data(context)
        return context

    def get_authenticated_context_data(self, context):
        return {
            **context,
            "emoji": EMOJI_CATEGORIES,
            "verbs": _get_verbs(self.request.user.username),
        }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields["recipe"].queryset = Recipe.objects.filter(
                created_by=self.request.user
            )
        return form
