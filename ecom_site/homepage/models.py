from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from datetime import date

# Create your models here.
class product_details(models.Model):
    item_code = models.CharField(max_length=20, null=True)
    item_name = models.CharField(max_length=30,null=True)
    item_quantity = models.CharField(max_length=10, null=True)
    price = models.FloatField(null=True)
    current_date = models.DateField(default=date.today)
    # image = models.ImageField(upload_to=None,height_field=None,width_field=None,max_length=None)
    def __str__(self):
        return self.item_name
    

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=32, null=True, blank=True)
    product = models.ForeignKey(product_details, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)