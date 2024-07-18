
from django.http import JsonResponse
import json
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .models import Product
from .forms import ProductForm
from.utils import cookieCart,cartData,guestOrder
from django.shortcuts import render, redirect, get_object_or_404
from .decorators import user_is_shreeys
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from .models import Customer  # Adjust this import based on your project structure
from .forms import AddToCartForm, ReviewForm
from .forms import ProductImageForm



def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create a Customer object for the newly created user
            Customer.objects.create(user=user)
            
            login(request, user)
            return redirect('store')  # Redirect to the store page or any other page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def store(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
        
    data = cartData(request)
    cartItems = data['cartItems'] 
    order = data['order']
    items = data['items']
    
    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        items = data['items']
            
            
        context = {'items':items, 'order':order,'cartItems':cartItems}
        return render(request, 'store/cart.html', context)

@login_required(login_url='/accounts/login/')
def checkout(request):
    data = cartData(request)
    context = {'items': data['items'], 'order': data['order'], 'cartItems': data['cartItems']}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)
   
from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
       

        
    else:
      
        customer,order = guestOrder(request,data)
                        
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        
        if total == float(order.get_cart_total):
            order.complete = True
        order.save()
        
        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],
                
            )             

    return JsonResponse('Payment complete', safe=False)

@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form = ProductForm()
    return render(request, 'store/add_product.html', {'form': form})




@login_required
@user_is_shreeys
# @user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    products = Product.objects.all()
    return render(request, 'store/admin_dashboard.html', {'products': products})

@user_passes_test(lambda u: u.is_superuser)
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'store/update_product.html', {'form': form})

@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_dashboard')
    return render(request, 'store/delete_product.html', {'product': product})



def search_results(request):
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()
    
    context = {
        'products': products,
        'query': query,
    }
    return render(request, 'store/search_result.html', context)

import logging

logger = logging.getLogger(__name__)

def product_detail(request, product_id):
    # Retrieve cart data
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    # Retrieve product or return 404 if not found
    product = get_object_or_404(Product, id=product_id)
    
    # Initialize forms
    form = AddToCartForm()
    review_form = ReviewForm()
    
    # Process POST requests
    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            form = AddToCartForm(request.POST)
            if form.is_valid():
                quantity = form.cleaned_data['quantity']
                
                # Update or initialize cart data from cookies
                cart = json.loads(request.COOKIES.get('cart', '{}'))
                if str(product.id) not in cart:
                    cart[str(product.id)] = {'quantity': 0}
                
                cart[str(product.id)]['quantity'] += quantity
                
                # Save updated cart in cookies
                response = redirect('cart')
                response.set_cookie('cart', json.dumps(cart))
                return response
            
        elif 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                if request.user.is_authenticated:
                    review = review_form.save(commit=False)
                    review.user = request.user
                    review.product = product
                    review.save()
                    return redirect('product_detail', product_id=product.id)
                else:
                    return redirect('login')
    
    # Context for rendering the template
    context = {
        'product': product,
        'form': form,
        'review_form': review_form,
        'reviews': product.reviews.all(),
        'cartItems': cartItems,
        'order': order,
        'items': items,
    }
    
    # Logging for debugging
    logger.debug(f'Product ID: {product.id}, Form Errors: {form.errors if form.errors else "None"}, Cart: {json.loads(request.COOKIES.get("cart", "{}"))}')
    
    return render(request, 'store/product_details.html', context)

def add_image(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.product = product
            image.color = form.cleaned_data['color']  # Ensure color is set
            image.save()
            return redirect('admin_dashboard')
    else:
        form = ProductImageForm()
    
    return render(request, 'store/add_image.html', {'form': form, 'product': product})
