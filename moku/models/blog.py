from django.db import models
from django.utils.translation import gettext_lazy as _

from moku.markdown import full_markdown


class BlogPost(models.Model):
    title = models.CharField(
        verbose_name=_("title"),
        max_length=128,
        help_text=_("the title of the blog post."),
    )
    text = models.TextField(
        verbose_name=_("content"),
        help_text=_("the content of the blog post. markdown is allowed here."),
    )
    created_by = models.ForeignKey(
        "User",
        related_name="+",
        db_column="created_by_user_id",
        on_delete=models.PROTECT,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def as_html(self):
        return full_markdown(self.text)
