from django.contrib import admin
from homepage.models import product_details,CartItem
# Register your models here.
admin.site.register(product_details)
admin.site.register(CartItem)