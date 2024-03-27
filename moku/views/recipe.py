from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy

from moku.forms.recipe import DeleteRecipeForm, RecipeForm, RecipeStepForm
from moku.models.recipe import Recipe, RecipeStep
from moku.views.base import FormView, View


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """Deletes a recipe from the database if it belongs to the authenticated user."""

    template_name = "moku/delete.jinja"
    form_class = DeleteRecipeForm

    def form_valid(self, form):
        self.recipe.delete()
        messages.success(self.request, _("recipe deleted successfully!"))
        return redirect("recipe.index")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "item": self.recipe.title,
            "back_url": reverse("recipe.show", kwargs={"uuid": self.recipe.uuid}),
        }

    @cached_property
    def recipe(self):
        return get_object_or_404(Recipe, uuid=self.kwargs.get("uuid"))

    def test_func(self):
        return self.request.user.id == self.recipe.created_by.id


class DeleteStepView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    Deletes a recipe step from the database if it belongs to the authenticated user.
    """

    def get(self, request, *args, **kwargs):
        if self.step.order != (self.step.recipe.steps.count() - 1):
            messages.error(self.request, _("sorry! you can only delete the last step."))
            return redirect(self.step.recipe.get_absolute_url())
        self.step.delete()
        messages.success(self.request, _("step deleted!"))
        return redirect(self.step.recipe.get_absolute_url())

    @cached_property
    def step(self):
        return get_object_or_404(
            RecipeStep,
            recipe__uuid=self.kwargs.get("uuid"),
            uuid=self.kwargs.get("step"),
        )

    def test_func(self):
        return self.request.user.id == self.step.recipe.created_by.id


class EditStepView(LoginRequiredMixin, UserPassesTestMixin, FormView):
    """Allows users to edit steps of a recipe they created."""

    template_name = "moku/recipe/edit_step.jinja"
    form_class = RecipeStepForm

    @property
    def page_title(self):
        return f"edit: step #{self.step.order + 1} of {self.step.recipe.title}"

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("step updated!"))
        return redirect(self.step.recipe.get_absolute_url())

    def get_form(self):
        return self.form_class(instance=self.step, **self.get_form_kwargs())

    @cached_property
    def step(self):
        return get_object_or_404(
            RecipeStep,
            recipe__uuid=self.kwargs.get("uuid"),
            uuid=self.kwargs.get("step"),
        )

    def test_func(self):
        return self.request.user.id == self.step.recipe.created_by.id


class IndexRecipeView(LoginRequiredMixin, View):
    """Shows a list of recipes created by the authenticated user."""

    template_name = "moku/recipe/index.jinja"
    page_title = gettext_lazy("my recipes")

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "recipes": Recipe.objects.filter(created_by=self.request.user).order_by(
                "-created_by"
            ),
        }


class NewRecipeView(LoginRequiredMixin, FormView):
    """Allows users to create a new recipe."""

    template_name = "moku/recipe/form.jinja"
    form_class = RecipeForm
    page_title = gettext_lazy("new recipe")

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(
            self.request,
            _("recipe made successfully! now you can start adding the steps."),
        )
        return redirect(form.instance.get_absolute_url())


class ShowRecipeView(FormView):
    """
    Shows users details about a recipe, and allows steps to be created for it if they
    are logged in as the recipe creator.
    """

    template_name = "moku/recipe/show.jinja"
    form_class = RecipeStepForm

    @property
    def page_title(self):
        return self.recipe.title

    @cached_property
    def recipe(self):
        return Recipe.objects.get(uuid=self.kwargs.get("uuid"))

    def form_valid(self, form):
        if (
            not self.request.user.is_authenticated
            or self.request.user.id != self.recipe.created_by.id
        ):
            messages.error(self.request, _("that's not yours!"))
            return redirect(form.instance.get_absolute_url())
        order = self.recipe.steps.count()
        if order >= 16:
            messages.error(
                self.request, _("sorry! you can't add any more steps to this recipe.")
            )
            return redirect(self.recipe.get_absolute_url())
        form.instance.recipe = self.recipe
        form.instance.order = order
        form.save()
        messages.success(self.request, _("step added successfully!"))
        return redirect(self.recipe.get_absolute_url())

    def get_context_data(self, **kwargs):
        return {**super().get_context_data(**kwargs), "recipe": self.recipe}
