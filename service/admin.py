from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from service.models import userinfo, Account, Location, Restaurant, FoodItem, Order, DeliveryMan,FinalDelivery

class AccountInline(admin.StackedInline):
    model = Account
    can_delete = False
    verbose_name_plural = 'Accounts'

class CustomizedUserAdmin(UserAdmin):
    inlines = (AccountInline, )

admin.site.unregister(User)
admin.site.register(User, CustomizedUserAdmin)

admin.site.register(userinfo)

class LocationAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'area']
    search_fields = ['user__username', 'area']

admin.site.register(Location, LocationAdmin)

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ['name', 'display_picture', 'rating', 'criteria', 'area']
    search_fields = ['name', 'area']

    def display_picture(self, obj):
        if obj.picture:
            return format_html('<img src="{}" width="300" height="150" />', obj.picture.url)
        return "No image"
    display_picture.short_description = 'Picture'

class FoodItemInline(admin.StackedInline):
    model = FoodItem
admin.site.register(FoodItem)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'restaurant', 'order_time', 'display_ordered_items']
    search_fields = ['user__username', 'restaurant__name']
    readonly_fields = ['order_id', 'order_time']

    def display_ordered_items(self, obj):
        return ', '.join([f"{item.food_item.name} ({item.quantity})" for item in obj.orderitem_set.all()])
    display_ordered_items.short_description = 'Ordered Items'

admin.site.register(DeliveryMan)
admin.site.register(FinalDelivery)
