from django.db import models
from django.conf import settings
from products.models import Product
# Create your models here.
class Order(models.Model):
    STATUS = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, choices=STATUS, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    def update_total_price(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super(OrderItem, self).save(*args, **kwargs)
        self.order.update_total_price()