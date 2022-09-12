from decimal import Decimal
from django_countries.fields import CountryField

from django.db import models
from django.conf import settings

from store.models import Product
from account.models import UserBase


ORDER_STATUS = [
    ('Created', 'Created'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Ready for pickup', 'Ready for pickup'),
    ('Completed', 'Completed')
]

TRANSPORT_CHOICES = [
    ('Courier delivery', 'Courier delivery'),
    ('Recipient pickup', 'Recipient pickup')
]


admin = UserBase.objects.get(username="admin")

class Order(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.CASCADE, related_name="orders", default=admin.id)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    telephone = models.CharField(max_length=20)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    country = CountryField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=20, choices=ORDER_STATUS, default='Created')
    note = models.TextField(blank=True)
    transport = models.CharField(max_length=20, choices=TRANSPORT_CHOICES)
    transport_cost = models.DecimalField(max_digits=10, decimal_places=2)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True, null=True)
    

    class Meta:
        ordering = ("-created",)

    def __str__(self):
        return str(self.created)


    def get_total_cost(self):
        all_order_items = self.order_items.all()
        total_cost = sum(order_item.get_cost()
                         for order_item in all_order_items)
        total_cost += self.transport_cost
        return total_cost




class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_order_items")
    price = models.DecimalField(max_digits=5, decimal_places=2)

    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.pk)

    def get_cost(self):
        return Decimal(self.price * self.quantity)
