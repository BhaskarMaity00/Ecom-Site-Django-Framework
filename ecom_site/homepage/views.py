from django.shortcuts import render,redirect
from homepage.models import product_details
from .models import CartItem
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
# for message flash
from django.contrib import messages
from datetime import date
  
# Create your views here.
def index(request): #   rendering templet with last 3 add products
    all_products = product_details.objects.all().order_by('-id')[:3]
    return render(request,'index.html',{'all_products':all_products})


def products(request):  # Fetch all products from database and render dynamically
    all_products = product_details.objects.all()
    return render(request,'product.html',{'all_products':all_products})

def signup(request):
    if request.method=="POST":
        # username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password1']
        confirm_password=request.POST['password2']

        if password!=confirm_password:
            messages.warning(request,"Password is Not Matching")
            return render(request,'signup.html')                   
        try:
            if User.objects.get(username=email):
                # return HttpResponse("email already exist")
                messages.info(request,"Email is Taken")
                return render(request,'signup.html')
        except Exception as identifier:
            pass
        user = User.objects.create_user(username=email,email=email,password=password)
        user.is_active=True
        user.save()
        return redirect('/login')
    return render(request,'signup.html')


# sign in
def handlelogin(request):
    if request.method=="POST":
        email=request.POST.get('email')
        userpassword=request.POST.get('password')
        myuser=authenticate(request,username=email,password=userpassword)
        if myuser is not None:
            login(request,myuser)
            # messages.success(request,"Login Success")
            return redirect('/home')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')

    return render(request,'login.html')

# logout
def handlelogout(request):
    logout(request)
    # messages.info(request,"Logout Success")
    return redirect('/')

# add to cart function
# def cart(request):
#     return render(request,'cart_templet/cart_page.html')


def add_to_cart(request,id):
    product=product_details.objects.get(id=id)
    user=request.user
    if request.user.is_authenticated:
        # If user is authenticated, associate the item with the user
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    else:
        # If user is not authenticated, associate the item with the session
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(session_key=session_key, product=product)

    # Update quantity 
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart_templet/cart_page.html', {'cart_items': cart_items})

def merge_carts(request):
    # If user is authenticated, update the user field for items associated with the session
    if request.user.is_authenticated:
        session_key = request.session.session_key
        CartItem.objects.filter(session_key=session_key).update(user=request.user)

    # Redirect to the view_cart page or another page as needed
    return redirect('view_cart')

def login_and_merge_carts(request):
    if request.method=="POST":
        email=request.POST.get('email')
        userpassword=request.POST.get('password')
        myuser=authenticate(request,username=email,password=userpassword)
        if myuser is not None:
            login(request,myuser)
            # After login, merge carts
            merge_carts(request)
            # messages.success(request,"Login Success")
            return redirect('/cart')

        else:
            messages.error(request,"Invalid Credentials")
            return redirect('/login')

    return render(request,'login.html')