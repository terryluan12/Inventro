from django.contrib import admin
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views
from dashboard import views as dash_views
from users import views as user_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),
    path("index.html", RedirectView.as_view(pattern_name="dashboard", permanent=False)),
    path("login", auth_views.LoginView.as_view(template_name="frontend/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("dashboard/", dash_views.index, name="dashboard"),
    path("inventory", dash_views.inventory, name="inventory"),
    path("cart", dash_views.cart, name="cart"),
    path("analytics", dash_views.analytics, name="analytics"),
    path("add-item/", dash_views.add_item, name="add_item"),
    path("inventory/edit/<int:pk>/", dash_views.edit_item, name="edit_item"),
    path("inventory/delete/<int:pk>/", dash_views.delete_item, name="delete_item"),
    path("users/add/", user_views.add_user, name="add_user"),
    path("api/metrics/", dash_views.metrics_api, name="metrics"),
]
