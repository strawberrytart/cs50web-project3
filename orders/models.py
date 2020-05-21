from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

# Create your models here.

# Salad model
class Salads(models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

# Pasta model
class Pasta(models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

# Toppings model
class Toppings(models.Model):
    name= models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

# Dinner Platters model 
class DinnerPlatters(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"

# Regular Pizza model 
class RegularPizza(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"

# Sicilian Pizza model 
class SicilianPizza(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"

# Subs model
class Subs(models.Model):
    name=models.CharField(max_length=64)
    small=models.DecimalField(max_digits=4, decimal_places=2)
    large=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.small} - {self.large}"

# Extra model
class Extra(models.Model):
    name=models.CharField(max_length=64)
    price=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.name}"

# Order model

class Order (models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    order_total=models.DecimalField(max_digits=8,decimal_places=2, default=0.00)
    status=models.CharField(max_length=64, default="Initiated")
    time=models.DateTimeField(auto_now=True,blank=True)

    def __str__(self):
        return f"{self.user} - {self.order_total} - {self.status} - {self.time.date()} - {self.time.time()}"

class OrderAdmin(admin.ModelAdmin):
    readonly_fields=('time',)

# Cart model 
class Cart (models.Model):
    order_id= models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_id")
    user=models.CharField(max_length=64)
    cart_item=models.CharField(max_length=64)
    toppings=models.ManyToManyField(Toppings, blank=True, related_name="cart_toppings")
    extras=models.ManyToManyField(Extra,blank=True, related_name="cart_extra")
    item_price=models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return f"{self.order_id.id}: {self.user} - {self.cart_item} - {self.toppings} - {self.extras} - {self.item_price}"

