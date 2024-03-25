from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import FormView, TemplateView
from django.utils.functional import cached_property
from django.utils.translation import gettext as _

from moku.forms.recipe import RecipeForm, RecipeStepForm
from moku.models.recipe import Recipe, RecipeStep


class DeleteRecipeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        self.recipe.delete()
        messages.success(self.request, _("recipe deleted successfully!"))
        return redirect("recipe.index")

    @cached_property
    def recipe(self):
        return get_object_or_404(
            Recipe,
            uuid=self.kwargs.get("uuid"),
        )

    def test_func(self):
        return self.request.user.id == self.recipe.created_by.id


class DeleteStepView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
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
    template_name = "moku/recipe/edit_step.jinja"
    form_class = RecipeStepForm

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


class IndexRecipeView(LoginRequiredMixin, TemplateView):
    template_name = "moku/recipe/index.jinja"

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "recipes": Recipe.objects.filter(created_by=self.request.user).order_by("-created_by"),
        }


class NewRecipeView(LoginRequiredMixin, FormView):
    template_name = "moku/recipe/form.jinja"
    form_class = RecipeForm

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.save()
        messages.success(self.request, _("recipe made successfully! now you can start adding the steps."))
        return redirect(form.instance.get_absolute_url())


class ShowRecipeView(FormView):
    template_name = "moku/recipe/show.jinja"
    form_class = RecipeStepForm

    @cached_property
    def recipe(self):
        return Recipe.objects.get(uuid=self.kwargs.get("uuid"))

    def form_valid(self, form):
        if not self.request.user.is_authenticated or self.request.user.id != self.recipe.created_by.id:
            messages.error(self.request, _("that's not yours!"))
            return redirect(form.instance.get_absolute_url())
        order = self.recipe.steps.count()
        if order >= 16:
            messages.error(self.request, _("sorry! you can't add any more steps to this recipe."))
            return redirect(self.recipe.get_absolute_url())
        form.instance.recipe = self.recipe
        form.instance.order = order
        form.save()
        messages.success(self.request, _("step added successfully!"))
        return redirect(self.recipe.get_absolute_url())

    def get_context_data(self, **kwargs):
        return {
            **super().get_context_data(**kwargs),
            "recipe": self.recipe,
        }
