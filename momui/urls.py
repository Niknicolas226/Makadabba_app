
# momui/urls.py
from django.urls import path
from .views import mom_signup, signup_success

urlpatterns = [
    path('signup/', mom_signup, name='mom_signup'),
    path('mom_signup/success/', signup_success, name='signup_success'),
    
]
