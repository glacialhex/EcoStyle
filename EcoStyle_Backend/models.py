from django.core.validators import MinLengthValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from EcoStyle import *


class User(AbstractUser):
    username = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(3)])
    password = models.CharField(max_length=100, validators=[MinLengthValidator(8)])
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username


class LoginEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.login_time}"


class Products(models.Model):
    Name = models.CharField(max_length=100)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    Description = models.TextField(max_length=500)
    ProductID = models.IntegerField(unique=True)
    Category = [
        ('Women', 'W'),
        ('Men', 'M'),
        ('Children', 'C'),
        ('Accessories', 'A'),
        ('Bags', 'B'),
        ('Home Decor', 'H'),
    ]
    Category = models.CharField(max_length=11, choices=Category)
    Size = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
    ]
    Size = models.CharField(max_length=2, choices=Size)

    def __str__(self):
        return self.Name


class Orders(models.Model):
    OrderID = models.IntegerField(unique=True)
    ProductID = models.ForeignKey(Products, on_delete=models.CASCADE)
    Quantity = models.IntegerField(default=1)
    TotalPrice = models.IntegerField(default=0)
    ShippingPrice = models.IntegerField(default=0)
    TotalQuantity = models.IntegerField(default=0)
    ShippingQuantity = models.IntegerField(default=0)
    User = models.ForeignKey(User, on_delete=models.CASCADE)  # Assuming you have implemented user authentication

    def __str__(self):
        return self.OrderID


class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('Bank', 'Bank'),
        ('PayPal', 'PayPal'),
        ('Cash On Delivery', 'Cash On Delivery'),
        ('Visa', 'Visa'),
        ('MasterCard', 'MasterCard'),
        ('Instapay', 'Instapay'),
        ('VF Cash', 'VF Cash'),
        ('Stripe', 'Stripe'),
    ]
    PaymentType = models.CharField(max_length=17, choices=PAYMENT_CHOICES)
    Amount = models.IntegerField()

    def __str__(self):
        return self.PaymentType


class ShippingInformation(models.Model):
    ShippingID = models.CharField(max_length=20, unique=True)
    Order = models.OneToOneField(Orders, on_delete=models.CASCADE)
    Address = models.CharField(max_length=200)
    City = models.CharField(max_length=100)


class PaymentLog(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"${self.amount} - {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
