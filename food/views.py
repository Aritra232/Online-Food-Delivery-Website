#from django.http import HttpResponse
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from service.models import userinfo, Location, Restaurant, FoodItem, Order, DeliveryMan, FinalDelivery,OrderItem
from django.contrib import messages
from django.template import loader
from django.db.models import Count
from django.core.exceptions import ValidationError
from django.core import serializers
import json
from decimal import Decimal
from datetime import datetime
from django.utils import timezone
import pytz

from django.http import JsonResponse
import json

from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

@login_required(login_url='login')
def foodpage(request):
    if request.method == "POST":
        address = request.POST.get('address')
        area = request.POST.get('area')
        Location.objects.update_or_create(user=request.user, defaults={'address': address, 'area': area})
        request.session['location_submitted'] = True  # Set or reset the flag upon submission
        return redirect('foodpage')
    else:
        location_submitted = request.session.get('location_submitted', False)
        location = Location.objects.filter(user=request.user).first() if location_submitted else None
        restaurants = Restaurant.objects.filter(area__iexact=location.area) if location and location_submitted else []

    return render(request, "food.html", {
        'location': location,
        'location_submitted': location_submitted,
        'restaurants': restaurants
    })







def logout_view(request):
    logout(request)
    request.session.pop('location_submitted', None)  # Clear the location submitted flag
    return redirect('login')

def restaurant_detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(pk=restaurant_id)
    food_items = FoodItem.objects.filter(restaurant=restaurant)

    if request.method == "POST":
        total_bill = 0
        for food_item in food_items:
            quantity = int(request.POST.get(f"quantity_{food_item.id}", 0))
            if quantity > 0:
                total_bill += food_item.price * quantity
        return render(request, "order_summary.html", {'restaurant': restaurant, 'total_bill': total_bill})

    return render(request, "restaurant_detail.html", {'restaurant': restaurant, 'food_items': food_items})

def order_summary(request):
    if request.method == "POST":
        restaurant_id = request.POST.get('restaurant_id')
        try:
            restaurant = Restaurant.objects.get(pk=restaurant_id)
        except Restaurant.DoesNotExist:
            return redirect('foodpage')
        
        total_bill = Decimal('0')
        ordered_items = {}
        for food_item in restaurant.fooditem_set.all():
            quantity = int(request.POST.get(f"quantity_{food_item.id}", 0))
            if quantity > 0:
                item_total = food_item.price * quantity
                total_bill += item_total
                ordered_items[food_item] = quantity

        # Calculate VAT
        vat = total_bill * Decimal('0.15')

        # Calculate total price with VAT and delivery price
        total_price_with_vat = total_bill + vat + Decimal('60')  # Add delivery price here

        subtotal = total_price_with_vat - 100
        # Fetch user's location if available
        user_location = None
        if request.user.is_authenticated:
            user_location = Location.objects.filter(user=request.user).first()

        # Get current time in Bangladesh timezone
        bangladesh_tz = pytz.timezone('Asia/Dhaka')
        current_time_bangladesh = datetime.now(bangladesh_tz)

        # Save order with all details
        order = Order.objects.create(
            user=request.user,
            restaurant=restaurant,
            quantity=sum(ordered_items.values()),
            total_bill=total_bill,
            vat=vat,
            total_price_with_vat=total_price_with_vat,
            subtotal = subtotal,
            location=user_location,
            order_time=current_time_bangladesh  # Set order time to current time in Bangladesh
        )

        # Associate food items with the order
        for food_item, quantity in ordered_items.items():
            order.orderitem_set.create(
                food_item=food_item,
                quantity=quantity
            )

        return render(request, "order_summary.html", {
            'user_location': user_location,
            'restaurant': restaurant, 
            'total_bill': total_bill,
            'vat': vat,
            'total_price_with_vat': total_price_with_vat,
            'subtotal' : subtotal,
            'ordered_items': ordered_items,
            'order_id': order.order_id,
            'order_time': current_time_bangladesh.strftime('%Y-%m-%d %H:%M:%S')  # Format order time for display
        })
    else:
        return redirect('confirmation')

def loginpage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        phone_number = request.POST.get('phone_number')

        # Check if a user with the provided username exists
        if User.objects.filter(username=username).exists():
            # Fetch the corresponding userinfo for the provided username
            delivery_info = DeliveryMan.objects.filter(username=username).first()
            
            # Check if userinfo exists and phone number matches
            if delivery_info is not None and str(delivery_info.phone_number) == phone_number:
                # Manually login the user
                user = User.objects.get(username=username)
                login(request, user)
                # Redirect to manpage with the username
                return redirect('manpage', username=user.username)
            else:
                user_info = userinfo.objects.filter(username=username).first()
                
                # Check if userinfo exists and phone number matches
                if user_info is not None and str(user_info.phone_number) == phone_number:
                    # Manually login the user
                    user = User.objects.get(username=username)
                    login(request, user)
                    # Redirect to foodpage
                    return redirect('foodpage')
                else:
                    return HttpResponse("Phone number doesn't match with the provided username.")
            
        else:
            return HttpResponse("Phone number doesn't match with the provided username.")
        
    return render(request, "log.html")

def manpage(request, username):
    user = User.objects.get(username=username)
    
    # Fetch orders that have not been accepted yet
    orders = Order.objects.filter(~Q(finaldelivery__isnull=False))
    
    return render(request, "man.html", {'first_name': user.first_name, 'last_name': user.last_name, 'orders': orders, 'username': username})

def signuppage(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone_number')  # Added for phone number
        first_name = request.POST.get('first_name')  # Added for first name
        last_name = request.POST.get('last_name')  # Added for last name

        # Check if username is already taken
        if User.objects.filter(username=uname).exists():
            return HttpResponse("Username already exists!")

        # Check if email is already registered
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already exists!")

        # Check if phone number is already registered in userinfo model
        if userinfo.objects.filter(phone_number=phone).exists():
            return HttpResponse("Phone number already exists!")

        # Create the user
        my_user = User.objects.create_user(username=uname, email=email, first_name=first_name, last_name=last_name)

        # Create a userinfo instance to store the phone number
        user_info = userinfo.objects.create(username=uname, phone_number=phone)

        # Associate the userinfo instance with the user
        my_user.userinfo = user_info
        my_user.save()

        return redirect('login')

    return render(request, "sign.html")

def logout_view(request):
    request.session.pop('location_submitted', None)  # Remove the session flag
    logout(request)
    return redirect('login')

def confirmation(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    final_delivery = FinalDelivery.objects.filter(order=order).first()

    if final_delivery:
        delivery_man = final_delivery.delivery_man
        delivery_man_info = get_object_or_404(DeliveryMan, username=delivery_man.username)
        order_items = OrderItem.objects.filter(order=order)
        context = {
            'order': order,
            'delivery_man': delivery_man,
            'delivery_man_phone': delivery_man_info.phone_number,
            'order_items': order_items,
            'accepted': True,
        }
    else:
        context = {
            'order': order,
            'delivery_man': None,
            'delivery_man_phone': None,
            'order_items': None,
            'accepted': False,
        }

    return render(request, 'confirmation.html', context)





from django.http import JsonResponse

def check_order_status(request, order_id):
    order = get_object_or_404(Order, order_id=order_id)
    final_delivery = FinalDelivery.objects.filter(order=order).first()
    accepted = final_delivery is not None
    response_data = {
        'accepted': accepted
    }
    return JsonResponse(response_data)










def accept_order(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        delivery_man_id = request.user.id
        order = get_object_or_404(Order, order_id=order_id)
        delivery_man = get_object_or_404(User, id=delivery_man_id)
        
        # Create FinalDelivery record
        final_delivery = FinalDelivery.objects.create(order=order, delivery_man=delivery_man)
        
        # If FinalDelivery creation is successful, flag the order as accepted
        if final_delivery:
            order.accepted = True
            order.save()
            return JsonResponse({'success': True, 'order_id': order_id})
        else:
            return JsonResponse({'success': False})
        
    return JsonResponse({'success': False})

def show_all_orders(request, username):
    delivery_man = get_object_or_404(User, username=username)
    final_deliveries = FinalDelivery.objects.filter(delivery_man=delivery_man)
    return render(request, 'show_all_orders.html', {'final_deliveries': final_deliveries})
