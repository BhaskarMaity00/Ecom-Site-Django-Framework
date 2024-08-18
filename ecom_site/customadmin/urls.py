from django.contrib import admin
from django.urls import path,include
from .views import *
# app_name='customadmin'
urlpatterns = [
    path('',admin_login,name='admin_login'),
    path('dashboard/',dashboard,name='dashboard'),
    path('admin_logout',admin_logout,name='admin_logout'),
    path('products/',products,name='products'),
    path('addproducts',addproducts,name='addproducts'),
    path('users/',user_list,name='users'),
    path('products/',products,name='products'),
    path('delete/<str:id>',delete,name='delete'),
    path('update/<str:id>',updateprod,name='update'),
    path('delete_user/<str:name>',delete_user,name='delete_user'),
    path('resetpassword',changepassword,name='resetpassword')
]