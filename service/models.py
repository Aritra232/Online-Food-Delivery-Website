from django.db import models
from django.contrib.auth.models import User
import random
import string

# Create your models here.
class userinfo(models.Model):
    username = models.CharField(max_length=20,null=True)
    phone_number = models.CharField(max_length=11, null=True,unique=True)

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nid = models.CharField(max_length=250, null=True)
    gender = models.CharField(
        max_length=6,
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    role = models.CharField(
        max_length=20,
        choices=[('Regular', 'Regular'), ('DeliveryMan', 'Delivery Man')],
        default='Regular'
    )

    def __str__(self):
        return self.user.username


class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    area = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username} - {self.area}"
    

class Restaurant(models.Model):
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='restaurants/')  # Stores images in MEDIA_ROOT/restaurants
    rating = models.FloatField()
    criteria = models.CharField(max_length=200)  # e.g., "Italian, Fast Food"
    area = models.CharField(max_length=100)  # The area the restaurant serves

    def __str__(self):
        return self.name


class FoodItem(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='food_items/')  # Stores images in MEDIA_ROOT/food_items
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ingredients = models.TextField()

    def __str__(self):
        return self.name
    

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    order_time = models.DateTimeField(auto_now_add=True)
    order_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    total_bill = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price_with_vat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.order_id} - {self.user.username}"

    def generate_order_id(self):
        characters = string.ascii_uppercase + string.digits
        order_id = ''.join(random.choices(characters, k=6))
        while Order.objects.filter(order_id=order_id).exists():
            order_id = ''.join(random.choices(characters, k=6))
        return order_id

    def save(self, *args, **kwargs):
        if not self.order_id:
            self.order_id = self.generate_order_id()
        super().save(*args, **kwargs)



class DeliveryMan(models.Model):
    username = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)


class FinalDelivery(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    delivery_man = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Order {self.order.order_id} - DeliveryMan {self.delivery_man.username}"