from django.shortcuts import redirect
from django.views.generic import FormView, TemplateView
from django.urls import reverse

from moku.forms.user import ProfileForm, UserForm
from moku.models.user import User


class EditProfileView(FormView):
    template_name = "moku/profile/edit.jinja"
    form_class = ProfileForm

    def form_valid(self, form):
        form.save()
        return redirect("profile", username=form.instance.username)

    def get_form(self):
        return self.form_class(instance=self.request.user, **self.get_form_kwargs())


class ProfileView(TemplateView):
    template_name = "moku/profile/show.jinja"

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.kwargs.get("username"))
        return {
            **super().get_context_data(**kwargs),
            "user": user,
            "posts": user.posts.order_by("-created_at").all(),
        }


class SignupView(FormView):
    template_name = "moku/signup.jinja"
    form_class = UserForm

    def get_success_url(self):
        return reverse("feed")
