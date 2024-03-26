import random

from django.views import generic


class View(generic.TemplateView):
    """Defines a common set of data to be passed to the template context."""

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "header_emoji": random.choice(
                ["🍔", "🍕", "🍟", "🥪", "🥘", "🍰", "🍻", "🧁", "🍞", "🥯", "🥐"]
            ),
        }


class FormView(View, generic.FormView):
    """Functions the same as `moku.views.base.View` but for rendering forms."""

    pass
