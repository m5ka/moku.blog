import random

from django.conf import settings
from django.views import generic


class View(generic.TemplateView):
    """Defines a common set of data to be passed to the template context."""

    page_title = None
    """The title of the current page. Should be overridden by subclasses."""

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "header_emoji": random.choice(
                ["🍔", "🍕", "🍟", "🥪", "🥘", "🍰", "🍻", "🧁", "🍞", "🥯", "🥐"]
            ),
            "site_root_url": settings.SITE_ROOT_URL,
            "page_title": self.page_title,
        }


class FormView(View, generic.FormView):
    """Functions the same as `moku.views.base.View` but for rendering forms."""

    pass
