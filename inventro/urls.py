from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from dashboard.views import index as dashboard_index, metrics_api
from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth
    path("login", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(next_page="/login"), name="logout"),

    # App
    path("dashboard/", dashboard_index, name="dashboard"),
    path("users/add/", user_views.add_user, name="add_user"),

    # Simple API used by the dashboard cards
    path("api/metrics/", metrics_api, name="metrics"),
]

# Optional: redirect bare root to /login
from django.views.generic import RedirectView
urlpatterns += [path("", RedirectView.as_view(url="/login", permanent=False))]
