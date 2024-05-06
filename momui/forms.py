# momui/forms.py
from django import forms
from .models import mom_signup

class SignUpForm(forms.ModelForm):
    class Meta:
        model = mom_signup
        fields = '__all__'
