import json

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import View as BaseView

from moku.constants import EMOJI_CATEGORIES, Verbs
from moku.forms.post import PostForm
from moku.images import process_post_image
from moku.models.post import Post
from moku.models.recipe import Recipe
from moku.views.base import FormView


class FeedView(FormView):
    template_name = "moku/feed.jinja"
    form_class = PostForm

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        if form.instance.recipe and form.instance.recipe.created_by.id != self.request.user.id:
            messages.error(self.request, _("you can't add someone else's recipe to your post!"))
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
            "posts": Post.objects.all()[:128]
        }
        if self.request.user.is_authenticated:
            return self.get_authenticated_context_data(context)
        return context

    def get_authenticated_context_data(self, context):
        return {
            **context,
            "emoji": EMOJI_CATEGORIES,
            "verbs": (
                (verb[0], verb[1] % {"user": f"@{self.request.user.username}", "food": "..."})
                for verb in Verbs.CHOICES
            )
        }

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if self.request.user.is_authenticated:
            form.fields["recipe"].queryset = Recipe.objects.filter(created_by=self.request.user)
        return form


class LatestPostJSONView(BaseView):
    def get(self, request, *args, **kwargs):
        post = Post.objects.prefetch_related("recipe__steps") \
                .filter(created_by__username=kwargs.get("username")) \
                .order_by("-created_at").first()
        if not post:
            return HttpResponse(json.dumps({"post": None}), content_type="application/json")
        post_data = {
            "date": str(post.created_at),
            "text": post.get_verb_display() % {"user": f"@{post.created_by.username}", "food": post.food},
            "food": post.food,
            "verb": {
                "id": post.verb,
                "pattern": post.get_verb_display() % {"user": "$1", "food": "$2"},
            },
            "image": f"{settings.SITE_ROOT_URL}{post.image.url}" if post.image else None,
            "user": {
                "username": post.created_by.username,
                "url": f"{settings.SITE_ROOT_URL}{post.created_by.get_absolute_url()}",
            },
        }
        if post.recipe:
            post_data["recipe"] = [step.instructions for step in post.recipe.steps.all()]
        return HttpResponse(json.dumps(post_data), content_type="application/json")
