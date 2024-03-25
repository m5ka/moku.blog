from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.utils.translation import gettext as _
from django.views.generic import FormView, TemplateView

from moku.images import process_avatar_image
from moku.forms.user import ProfileForm, UserForm
from moku.models.user import User


class EditProfileView(LoginRequiredMixin, FormView):
    template_name = "moku/profile/edit.jinja"
    form_class = ProfileForm

    def form_valid(self, form):
        if "avatar" in form.changed_data and form.instance.avatar is not None:
            form.instance.avatar = process_avatar_image(form.instance.avatar)
        form.save()
        messages.success(self.request, _("profile updated successfully!"))
        return redirect("profile", username=form.instance.username)

    def get_form(self):
        return self.form_class(instance=self.request.user, **self.get_form_kwargs())


class ProfileView(TemplateView):
    template_name = "moku/profile/show.jinja"

    def get_context_data(self, **kwargs):
        user = User.objects.get(username=self.kwargs.get("username"))
        return {
            **super().get_context_data(**kwargs),
            "profile": user,
            "posts": user.posts.order_by("-created_at").all(),
        }


class SignupView(FormView):
    template_name = "moku/signup.jinja"
    form_class = UserForm

    def form_valid(self, form):
        form.save()
        messages.success(self.request, _("that's it! just log in, and you're ready to go."))
        return redirect("login")

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("feed")
        return super().get(request, *args, **kwargs)
