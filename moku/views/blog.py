from django.utils.translation import gettext_lazy

from moku.models.blog import BlogPost
from moku.views.base import View


class IndexBlogView(View):
    template_name = "moku/blog.jinja"
    page_title = gettext_lazy("blog")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "posts": BlogPost.objects.order_by("-created_at").all(),
        }
