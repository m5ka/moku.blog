"""
URL configuration for moku project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from moku.views.auth import LoginView, LogoutView
from moku.views.post import FeedView, LatestPostJSONView
from moku.views.recipe import (
    DeleteRecipeView,
    DeleteStepView,
    EditStepView,
    IndexRecipeView,
    NewRecipeView,
    ShowRecipeView,
)
from moku.views.static import ChangelogView, PrivacyView, TermsView
from moku.views.user import EditProfileView, EditSettingsView, ProfileView, SignupView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", FeedView.as_view(), name="feed"),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path("signup", SignupView.as_view(), name="signup"),
    path("profile", EditProfileView.as_view(), name="profile.edit"),
    path("settings", EditSettingsView.as_view(), name="settings"),
    path("changelog", ChangelogView.as_view(), name="changelog"),
    path("privacy", PrivacyView.as_view(), name="privacy"),
    path("terms", TermsView.as_view(), name="terms"),
    path("user/<str:username>", ProfileView.as_view(), name="profile"),
    path("user/<str:username>/json", LatestPostJSONView.as_view(), name="json"),
    path("recipes", IndexRecipeView.as_view(), name="recipe.index"),
    path("recipes/new", NewRecipeView.as_view(), name="recipe.new"),
    path("recipes/<str:uuid>", ShowRecipeView.as_view(), name="recipe.show"),
    path("recipes/<str:uuid>/delete", DeleteRecipeView.as_view(), name="recipe.delete"),
    path("recipes/<str:uuid>/<str:step>", EditStepView.as_view(), name="step.edit"),
    path("recipes/<str:uuid>/<str:step>/delete", DeleteStepView.as_view(), name="step.delete"),
]

if settings.DEBUG_TOOLBAR:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
