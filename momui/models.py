# momui/models.py
from django.db import models

class mom_signup(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    dietary_restrictions = models.CharField(max_length=100, blank=True)
    cuisine_preferences = models.CharField(max_length=100, blank=True)
    allergies = models.CharField(max_length=100, blank=True)
    preferred_delivery_time = models.TimeField()
    delivery_frequency = models.CharField(max_length=20)
    people_served = models.IntegerField()
    comments = models.TextField(blank=True)


    def __str__(self):
        return self.full_name