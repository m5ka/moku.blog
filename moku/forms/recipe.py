from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from moku.models.recipe import Recipe, RecipeStep


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ("title",)
        labels = {"title": _("recipe title")}


class RecipeStepForm(ModelForm):
    class Meta:
        model = RecipeStep
        fields = ("instructions",)
