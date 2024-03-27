from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from moku.views.auth import LoginView, LogoutView
from moku.views.blog import IndexBlogView
from moku.views.post import FeedView
from moku.views.recipe import (
    DeleteRecipeView,
    DeleteStepView,
    EditStepView,
    IndexRecipeView,
    NewRecipeView,
    ShowRecipeView,
)
from moku.views.static import PrivacyView, TermsView
from moku.views.user import (
    EditProfileView,
    EditSettingsView,
    ProfileView,
    SignupView,
    UserJSONView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", FeedView.as_view(), name="feed"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("profile", EditProfileView.as_view(), name="profile.edit"),
    path("settings", EditSettingsView.as_view(), name="settings"),
    path("blog", IndexBlogView.as_view(), name="blog.index"),
    path("privacy", PrivacyView.as_view(), name="privacy"),
    path("terms", TermsView.as_view(), name="terms"),
    path("user/<str:username>", ProfileView.as_view(), name="profile"),
    path("user/<str:username>/json", UserJSONView.as_view(), name="json"),
    path("recipes", IndexRecipeView.as_view(), name="recipe.index"),
    path("recipes/new", NewRecipeView.as_view(), name="recipe.new"),
    path("recipes/<str:uuid>", ShowRecipeView.as_view(), name="recipe.show"),
    path("recipes/<str:uuid>/delete", DeleteRecipeView.as_view(), name="recipe.delete"),
    path("recipes/<str:uuid>/<str:step>", EditStepView.as_view(), name="step.edit"),
    path(
        "recipes/<str:uuid>/<str:step>/delete",
        DeleteStepView.as_view(),
        name="step.delete",
    ),
]
"""
URL patterns, defining the routes available in moku.blog.
More information: https://docs.djangoproject.com/en/5.0/topics/http/urls/
"""

if settings.DEBUG_TOOLBAR:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
