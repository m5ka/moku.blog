from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.utils.translation import gettext as _

from moku.constants import EMOJI_CATEGORIES, Verbs
from moku.forms.post import PostForm
from moku.images import process_post_image
from moku.models.post import Post
from moku.models.recipe import Recipe
from moku.views.base import FormView


class FeedView(FormView):
    """Allows users to see recent posts and create a new post."""

    template_name = "moku/feed.jinja"
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
        if "image" in form.changed_data and form.instance.image is not None:
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
            "verbs": (
                (
                    verb[0],
                    verb[1] % {"user": f"@{self.request.user.username}", "food": "..."},
                )
                for verb in Verbs.CHOICES
            ),
        }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields["recipe"].queryset = Recipe.objects.filter(
                created_by=self.request.user
            )
        return form
