from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from products.views import ItemViewSet
from cart.views import CartViewSet
from dashboard import views as dash_views

router = DefaultRouter()
router.register(r"items", ItemViewSet, basename="item")
router.register(r"cart", CartViewSet, basename="cart")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),

    # Built-in auth endpoints (/accounts/login etc) – optional but handy for admin
    path("accounts/", include("django.contrib.auth.urls")),

    # Explicit friendly login/logout so your templates can link to /login and /logout
    path("login", dash_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("logout", dash_views.LogoutView.as_view(), name="logout"),

    # Dashboard + pages
    path("", include("dashboard.urls")),

    # Metrics for the frontend JS client (and tests)
    path("api/metrics/", dash_views.metrics_api, name="metrics"),
]
