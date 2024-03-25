from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from moku.models import Post


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ("emoji", "verb", "food", "image")
        labels = {
            "emoji": _("emoji"),
            "verb": _("verb"),
            "food": _("food"),
            "image": _("image"),
        }
