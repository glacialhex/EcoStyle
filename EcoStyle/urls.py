from django.contrib import admin
from django.urls import path
from EcoStyle_Backend.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('main/', main_page, name='main_page'),
    path('register/', user_registration, name='user_registration'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='user_logout'),
    path('category/<str:category>/', category_products, name='category_products'),
    path('bags/', bags, name='bags'),
    path('accessories/', accessories, name='accessories'),
    path('kids/', kids, name='kids'),
    path('home/', home, name='home'),
    path('men/', men, name='men'),
    path('women/', women, name='women'),
    path('payment/', payment, name='payment'),
    path('confirm_payment/', confirm_payment, name='confirm_payment'),
    path('thank_you/<int:order_id>/', thank_you_page, name='thank_you_page'),
    path('contact/', contact, name='contact'),
    path('message/', message, name='message'),
]
