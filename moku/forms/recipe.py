from django.forms import Form, ModelForm
from django.utils.translation import gettext_lazy as _

from moku.models.recipe import Recipe, RecipeStep


class DeleteRecipeForm(Form):
    pass


class RecipeForm(ModelForm):
    """Form for creating and updating recipes."""

    class Meta:
        model = Recipe
        fields = ("title",)
        labels = {"title": _("recipe title")}


class RecipeStepForm(ModelForm):
    """Form for creating and updating steps of a recipe."""

    class Meta:
        model = RecipeStep
        fields = ("instructions",)
