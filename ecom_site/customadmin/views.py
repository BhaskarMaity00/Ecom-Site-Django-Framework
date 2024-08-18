from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from homepage.models import product_details
# from .models import CustomUser
from django.utils import timezone
# Create your views here.

# function for admin login page
def admin_login(request):
    try:
        if request.user.is_authenticated:
            return redirect('dashboard/')
        if request.method == 'POST':
            username = request.POST.get("username")
            password = request.POST.get("password")
            user_obj = User.objects.filter(username = username)
            if not user_obj.exists():
                messages.info(request,'Account not found!')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            user_obj = authenticate(request,username = username,password = password)
            if user_obj and user_obj.is_superuser:
                login(request , user_obj)
                return redirect('dashboard/')
            
            messages.info(request, 'Invalid Password!')
            return render(request,'admin_login.html')
        return render(request,'admin_login.html')
    except Exception as e:
        print(e)

# logout function
def admin_logout(request):
    logout(request)
    messages.success(request,"Logging Out Successfully!")
    return redirect('admin_login')

@login_required(login_url='admin/')  # Redirect to the login page if not authenticated
def dashboard(request):
    # get current month and year
    # current_month = timezone.now().month
    # current_year = timezone.now().year
    users = User.objects.all()
    products = product_details.objects.all().order_by('-id')[:3]
    total_user = sum(1 for user in users if user.is_superuser==False)
    # current_user = CustomUser.objects.all()
    # print(current_user)
    content={
        'total_user':total_user,
        # 'current_user':current_user,
        'products':products
    }
    return render(request,'html/index.html',content)

def products(request): #    Fetch all products from database and render dynamically
    all_products = product_details.objects.all()
    return render(request,'html/products.html',{'all_products':all_products})

def addproducts(request):   # add products page
    if request.method == 'POST':
        item_code = request.POST.get('item_code')
        item_name = request.POST.get('item_name')
        item_quantity = request.POST.get('item_quantity')
        item_price = request.POST.get('item_price')
        add_product = product_details(item_code=item_code,item_name=item_name,item_quantity=item_quantity,price=item_price)
        add_product.save()
        messages.success(request,"Product Added Successfully!")
    return render(request,'html/prod_regis.html')

# list of users
def user_list(request):
    users = User.objects.all()
    for user in users:
        if user.is_active==True:
            user.is_active='Activated'
            if user.is_staff==True:
                user.status='Admin'
            elif user.is_superuser==True:
                user.status='SuperUser'
            else:
                user.status='Member'
        else:
            user.is_active='Banned'
    return render(request,'html/user_list.html',{'users':users})
def delete_user(request,name):
    user=get_object_or_404(User,username=name)
    user.delete()
    messages.success(request,'User deleted successfully!')
    # users=User.objects.all()
    return redirect('users')
# edit products
def products(request):
    all_products = product_details.objects.all()
    return render(request,'html/allproduct.html',{'all_products':all_products})

# update products
def updateprod(request,id):
    # all_products = product_details.objects.all()
    product = get_object_or_404(product_details,id=id)
    if request.method=='POST':
        item_code=request.POST.get('item_code')
        item_name=request.POST.get('item_name')
        item_quantity=request.POST.get('item_quantity')
        item_price=request.POST.get('item_price')
        add_product = product_details(
            id=id,
            item_code=item_code,
            item_name=item_name,
            item_quantity=item_quantity,
            price=item_price
            )
        add_product.save()
        messages.success(request,"Product Updated Successfully!")
        return redirect('products')
    else:
        return render(request,'html/edit_product.html',{'product':product})
    
def delete(request,id):
    product = get_object_or_404(product_details,id=id)
    product.delete()
    messages.success(request,"Product deleted successfully!")
    return redirect('products')

# function for password change
def changepassword(request):
    if request.method =='POST':
        old_password = request.POST.get('old_password')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmPassword')
        user = User.objects.filter(username=request.user)
        if password1 != password2:
            messages.info(request,"Password is not Matching!")
            return redirect('resetpassword')
        elif authenticate(request,username = request.user.username,password = old_password):
            user[0].set_password(password1)
            user[0].save()
            messages.success(request,"Password Changes Successfully!")
            return redirect('resetpassword')
        else:
            messages.info(request,"Old password is wrong!")
            return redirect('resetpassword')
    return render(request,'html/change_password.html')

