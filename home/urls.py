"""
URL configuration for pilot project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from home import views
from django.conf import settings
from django.conf.urls.static import static
from .views import menu, home_signup, activate, signin, signout, menuweek

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.home_signup, name='home_signup'),
    path('subscription/signupmonth/', views.home_signup, name='signup'),
    path('activate/<uidb64>/<token>', views.activate, name='activate'),
    path('signin/', views.signin, name='signin'),
    path('menu/', views.menu, name='menu'),
    path('menu/signupna', views.home_signup, name='signup'),
    path('signout', views.signout, name='signout'),
    path('signin/view-profile', views.view_profile, name='view_profile'),
    path('userui/menu', views.menu, name='menu'),
    path('userui/view_cart', views.view_cart, name='view_cart'),
    path('userui/profile', views.profile, name='profile'),
    path('userui/view-profile', views.view_profile, name='view_profile'),
    path('userui/edit-profile', views.edit_profile, name='edit_profile'),
    path('menuweek/', views.menuweek, name='menuweek'),
    path('userui/', views.userui, name='userui'),
    path('signin/menu/', views.menu, name='menu'),
    path('momreg/', views.momreg, name='momreg'),
    path('subscription/', views.subscription, name='subscription'),
    path('accounts/login/', views.custom_login, name='login'),
    path('payment_gateway/', views.payment_gateway, name='payment_gateway'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('view_cart/', views.view_cart, name='view_cart'),  # URL for viewing the cart
    path('add_to_cart/<int:menu_item_id>/', views.add_to_cart, name='add_to_cart'),  # URL for adding an item to the cart
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),  # URL for removing an item from the cart
   
    

    
    
]
