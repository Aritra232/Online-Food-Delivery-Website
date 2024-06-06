"""
URL configuration for food project.

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
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.signuppage,name='sign'),
    path('login', views.loginpage,name='login'),
    path('foodpage', views.foodpage,name='foodpage'),
    path('logout/', views.logout_view, name='logout'),
    path('restaurant/<int:restaurant_id>/', views.restaurant_detail, name='restaurant_detail'),
    path('order_summary/', views.order_summary, name='order_summary'),  # Add this line
    path('confirmation/<str:order_id>/', views.confirmation, name='confirmation'),
    path('manpage/<str:username>/', views.manpage, name='manpage'),
    path('accept_order/', views.accept_order, name='accept_order'),
    path('show_all_orders/<str:username>/', views.show_all_orders, name='show_all_orders'),
    path('check_order_status/<str:order_id>/', views.check_order_status, name='check_order_status'),  # New endpoint
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
