from django import forms
from .models import Profile

class MotherLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class MotherSignupForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    dietary_restrictions = forms.CharField(max_length=200, required=False)
    cuisine_preferences = forms.CharField(max_length=200, required=False)
    allergies = forms.CharField(max_length=200, required=False)
    preferred_delivery_time = forms.TimeField()
    delivery_frequency = forms.ChoiceField(choices=[('daily', 'Daily'), ('weekly', 'Weekly'), ('bi-weekly', 'Bi-weekly')])
    people_served = forms.IntegerField()
    comments = forms.CharField(widget=forms.Textarea, required=False)



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'address', 'phone', 'email', 'gender']


class PaymentForm(forms.Form):
    payment_method = forms.ChoiceField(choices=(
        ('cash', 'Cash on Delivery'),
        ('online', 'Online Payment'),
    ))
    name = forms.CharField(max_length=100, label='Name on Card')
    card_number = forms.CharField(max_length=16, label='Card Number')
    expiry_date = forms.DateField(label='Expiry Date')
    cvv = forms.CharField(max_length=4, label='CVV')