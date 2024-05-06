# momui/admin.py
# momui/admin.py
from django.contrib import admin
from .models import  mom_signup

@admin.register(mom_signup)
class MomSignUpAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'address', 'preferred_delivery_time', 'delivery_frequency')
    search_fields = ('full_name', 'email', 'phone_number', 'address')
    list_filter = ('preferred_delivery_time', 'delivery_frequency')


