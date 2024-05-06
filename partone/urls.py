# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('pricing/', views.pricing_view, name='pricing'),
    path('settings/', views.settings_view, name='settings'),
    path('customer-care/', views.customer_care_view, name='customer_care'),
    path('how-we-deliver/', views.delivery_view, name='delivery'),
    path('submit/', views.submit_query, name='submit_query'),
    path('success/', views.query_success, name='query_success'),
    path('our-commitment/', views.our_commitment, name='our_commitment'),

]
