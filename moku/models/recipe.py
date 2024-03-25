from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from shortuuid.django_fields import ShortUUIDField


class RecipeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset() \
            .prefetch_related(
                models.Prefetch("steps", queryset=RecipeStep.objects.order_by("order"))
            )


class Recipe(models.Model):
    uuid = ShortUUIDField(
        verbose_name=_("unique id"),
        max_length=22,
        length=22,
        help_text=_("the unique id that identifies this recipe."),
    )
    title = models.CharField(
        verbose_name=_("recipe title"),
        max_length=64,
        help_text=_("give the recipe a title, just so you know the recipe is for."),
    )
    created_by = models.ForeignKey(
        "User",
        related_name="recipes",
        db_index=True,
        db_column="created_by_user_id",
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    objects = RecipeManager()

    def __str__(self):
        return f"{self.title} by @{self.created_by.username}"

    def get_absolute_url(self):
        return reverse("recipe.show", kwargs={"uuid": self.uuid})


class RecipeStep(models.Model):
    uuid = ShortUUIDField(
        verbose_name=_("step id"),
        max_length=22,
        length=22,
        help_text=_("the unique id that identifies this step."),
    )
    instructions = models.CharField(
        verbose_name=_("step instructions"),
        max_length=128,
        help_text=_("the instructions for this step of the recipe. try to keep it clear and concise!"),
    )
    order = models.IntegerField(
        verbose_name=_("step number"),
        default=0,
        db_index=True,
        help_text=_("which step in the recipe is this. this affects the order the recipe steps are shown."),
    )
    recipe = models.ForeignKey(
        "Recipe",
        related_name="steps",
        db_index=True,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"step #{self.order + 1} of {self.recipe}"
