# inventro/urls.py
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from dashboard import views as dash_views
from users import views as user_views  # keeps add_user view

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home -> login
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    # Handle old /index.html hits (from stale links)
    path("index.html", RedirectView.as_view(pattern_name="dashboard", permanent=False)),

    # Auth using Django built-ins
    path(
        "login",
        auth_views.LoginView.as_view(template_name="frontend/login.html"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),

    # App views
    path("dashboard/", dash_views.index, name="dashboard"),
    path("users/add/", user_views.add_user, name="add_user"),

    # API
    path("api/metrics/", dash_views.metrics_api, name="metrics"),
]
