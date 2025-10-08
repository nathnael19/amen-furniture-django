from django.db import models
import uuid
from django.conf import settings
from products.models import Product
from django.db.models import Sum, F, DecimalField

class Cart(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total(self):
        result = self.items.aggregate(
            total=Sum(F("product__price") * F("quantity"), output_field=DecimalField())
        )
        return result["total"] or 0

    def __str__(self):
        return f"Cart {self.pk} ({self.user or 'Guest'})"


class CartItem(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
