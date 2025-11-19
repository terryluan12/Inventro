from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from dashboard import views as dash_views
from users import views as user_views  # for add_user

urlpatterns = [
    path("admin/", admin.site.urls),

    # Redirect root to login
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),

    # Redirect old /index.html to dashboard
    path("index.html", RedirectView.as_view(pattern_name="dashboard", permanent=False)),

    # Login/Logout using built-in auth views and your template
    path("login", auth_views.LoginView.as_view(template_name="frontend/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(next_page="login"), name="logout"),

    # Main dashboard
    path("dashboard/", dash_views.index, name="dashboard"),

    # Public inventory & cart routes
    path("inventory", dash_views.inventory, name="inventory"),
    path("cart", dash_views.cart, name="cart"),

    # Analytics page for dashboard statistics
    path("analytics", dash_views.analytics, name="analytics"),

    # Inventory CRUD routes
    path("add-item/", dash_views.add_item, name="add_item"),
    path("inventory/edit/<int:pk>/", dash_views.edit_item, name="edit_item"),
    path("inventory/delete/<int:pk>/", dash_views.delete_item, name="delete_item"),

    # Add user (superuser only)
    path("users/add/", user_views.add_user, name="add_user"),

    # API endpoint for dashboard stats
    path("api/metrics/", dash_views.metrics_api, name="metrics"),
]
