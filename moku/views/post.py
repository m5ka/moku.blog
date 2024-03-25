from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import FormView

from moku.constants import EMOJI_CATEGORIES, Verbs
from moku.models.post import Post
from moku.forms.post import PostForm


class FeedView(FormView):
    template_name = "moku/feed.jinja"
    form_class = PostForm

    def form_valid(self, form):
        if not self.request.user.is_authenticated:
            raise PermissionDenied
        form.instance.created_by = self.request.user
        form.instance.save()
        return redirect("feed")

    def get_context_data(self, **kwargs):
        context = {
            **super().get_context_data(**kwargs),
            "posts": Post.objects.order_by("-created_at").all()[:128]
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
