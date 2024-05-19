from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, PaymentForm
from django.http import JsonResponse
from .models import Products, LoginEvent, Orders, ShippingInformation, PaymentLog
from datetime import datetime
import random


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'You have been successfully logged in.')
            LoginEvent.objects.create(user=user)
            next_url = request.POST.get('next') or 'index.html'
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('index')


def user_registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}. You can now log in.')
            return redirect('login.html')
    else:
        form = UserRegistrationForm()
    return render(request, 'reg.html', {'form': form})


def category_products(request, category):
    if request.method == 'GET':
        try:
            products = Products.objects.filter(category=category)
            product_list = [product.name for product in products]
            return JsonResponse(product_list, safe=False)
        except Products.DoesNotExist:
            return JsonResponse({'message': 'Category not found'}, status=404)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)


def main_page(request):
    if request.method == 'GET':
        main_page_contents = {
            'Men': Products.objects.filter(Category='Men').values_list('Name', flat=True),
            'Women': Products.objects.filter(Category='Women').values_list('Name', flat=True),
            'Kids': Products.objects.filter(Category='Kids').values_list('Name', flat=True),
            'Bags': Products.objects.filter(Category='Bags').values_list('Name', flat=True),
            'Accessories': Products.objects.filter(Category='Accessories').values_list('Name', flat=True),
            'Home_Decor': Products.objects.filter(Category='Home Decor').values_list('Name', flat=True),
        }
        return render(request, 'indexmain.html', main_page_contents)
    else:
        return JsonResponse({'message': 'Method not allowed'}, status=405)




def bags(request):
    bag_products = Products.objects.filter(Category='Bags')
    return render(request, 'bags.html', {'bag_products': bag_products})


def accessories(request):
    accessory_products = Products.objects.filter(Category='Accessories')
    return render(request, 'accessories.html', {'accessory_products': accessory_products})


def kids(request):
    kids_products = Products.objects.filter(Category='Kids')
    return render(request, 'kids.html', {'kids_products': kids_products})


def home(request):
    home_products = Products.objects.filter(Category='Home')
    return render(request, 'home.html', {'home_products': home_products})


def men(request):
    men_products = Products.objects.filter(Category='Men')
    return render(request, 'men.html', {'men_products': men_products})


def women(request):
    women_products = Products.objects.filter(Category='Women')
    return render(request, 'women.html', {'women_products': women_products})


def payment(request):
    current_year = datetime.now().year
    years = [str(year) for year in range(current_year, current_year + 11)]
    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            log_payment(cleaned_data)
            #f"Payment processed for card ending with {card_number[-4:]}")
            return redirect('thank.html')
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {'form': form, 'months': months, 'years': years})


def log_payment(payment_data):
    amount = 100  # Example amount, replace with actual value from form or elsewhere
    PaymentLog.objects.create(amount=amount)
    payment_data['amount'] = amount


def confirm_payment(request):
    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            order = Orders.objects.create(
                OrderID=random.randint(100000, 999999),
                ProductID=Products.ProductID,
                Quantity=1,
                TotalPrice=0,
                ShippingPrice=0,
                TotalQuantity=0,
                ShippingQuantity=0,
                User=request.user
            )
            ShippingInformation.objects.create(
                Order=order,
                Address=request.POST.get('homeAddress'),
                City=request.POST.get('cityName')
            )
            return redirect('thank', order_id=order.OrderID)
    else:
        form = PaymentForm()
    return render(request, 'payment.html', {'form': form})


def thank_you_page(request, order_id):
    order = Orders.objects.get(OrderID=order_id)
    return render(request, 'thank.html',
                  {'order_id': order.OrderID, 'shipping_id': order.shippinginformation.shippingID[-4:]})


def contact(request):
    return render(request, 'contact.html')


def message(request):
    return render(request, 'message.html')
