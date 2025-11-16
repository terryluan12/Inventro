from django.conf import settings
from django.db import models

class Cart(models.Model):
    # Use the real auth user model (defaults to django.contrib.auth.models.User)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="carts"
    )
    # Keep your chosen structure; list of {"sku": "...", "qty": N} works fine
    items = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Cart #{self.pk} for {self.user}"
