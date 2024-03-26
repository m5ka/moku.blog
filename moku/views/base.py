import random

from django.views import generic


class View(generic.TemplateView):
    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "header_emoji": random.choice(
                ["🍔", "🍕", "🍟", "🥪", "🥘", "🍰", "🍻", "🧁", "🍞", "🥯", "🥐"]
            ),
        }


class FormView(View, generic.FormView):
    pass
