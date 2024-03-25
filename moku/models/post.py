from django.db import models
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from shortuuid.django_fields import ShortUUIDField

from moku.constants import Verbs
from moku.validators import validate_emoji


def post_image_filename(instance, _):
    return f"posts/{instance.created_by.username}__{instance.uuid}.webp"


class Post(models.Model):
    uuid = ShortUUIDField(
        verbose_name=_("unique id"),
        max_length=22,
        length=22,
        help_text=_("the unique id that identifies this post."),
    )
    emoji = models.CharField(
        verbose_name=_("emoji"),
        max_length=8,
        validators=[validate_emoji],
        help_text=_("an emoji to accompany your post!"),
    )
    verb = models.CharField(
        verbose_name=_("verb"),
        max_length=32,
        choices=Verbs.CHOICES,
        help_text=_("how should we best phrase this entry?"),
    )
    food = models.CharField(
        verbose_name=_("food"),
        max_length=128,
        help_text=_("what did you eat?"),
    )
    image = models.ImageField(
        verbose_name=_("image"),
        blank=True,
        upload_to=post_image_filename,
        help_text=_("here you can upload a picture of what you ate!"),
    )
    created_by = models.ForeignKey(
        "User",
        related_name="posts",
        db_index=True,
        db_column="created_by_user_id",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text=_("when this post was created."),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text=_("when this post was last updated."),
    )

    def __str__(self):
        return f"{self.text} on {self.created_at}"

    @property
    def text(self):
        return self.get_verb_display() % {
            "user": f"<a href=\"{self.created_by.get_absolute_url()}\">@{self.created_by.username}</a>",
            "food": escape(self.food),
        }
