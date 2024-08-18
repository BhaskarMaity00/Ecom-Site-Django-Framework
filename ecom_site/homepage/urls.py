"""
URL configuration for ecom_site project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from homepage import views

urlpatterns = [
    path("",views.index,name='homepage'),
    path("home",views.index,name='homepage'),
    path("product",views.products,name='product'),
    path('login',views.handlelogin,name='login'),
    path('signup',views.signup,name='signup'),
    # path('cart/',views.cart,name='cart'),
    path('addTocart/<str:id>',views.add_to_cart,name='add_to_cart'),
    path('logout',views.handlelogout,name='logout'),
    path('add_to_cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('login_and_merge_carts/', views.login_and_merge_carts, name='login_and_merge_carts'),
]
