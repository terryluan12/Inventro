# inventro/urls.py
from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

from dashboard import views as dash_views
from users import views as user_views  # for add_user

urlpatterns = [
    path("admin/", admin.site.urls),

    # Home -> login
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),

    # Handle stale links that go to /index.html (redirect to dashboard once logged in)
    path("index.html", RedirectView.as_view(pattern_name="dashboard", permanent=False)),

    # Auth using Django's built-ins and your login template
    path("login",  auth_views.LoginView.as_view(template_name="frontend/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # App views
    path("dashboard/", dash_views.index, name="dashboard"),
    path("users/add/", user_views.add_user, name="add_user"),

    # API
    path("api/metrics/", dash_views.metrics_api, name="metrics"),
]
