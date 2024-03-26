from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from moku import models

for model_name in models.__all__:
    model = getattr(models, model_name)
    if model.__name__ != "User":
        admin.site.register(model)


@admin.register(models.User)
class UserAdmin(BaseUserAdmin):
    """Admin class override for the User model."""

    fieldsets = (
        (None, {"fields": ("username", "email", "password")}),
        ("Profile", {"fields": ("pronouns", "location", "bio")}),
        ("Status", {"fields": ("email_confirmed_at",)}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Dates", {"fields": ("date_joined", "last_seen_at")}),
    )
