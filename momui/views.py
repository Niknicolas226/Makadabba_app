from django.shortcuts import render, redirect
from .forms import SignUpForm

def mom_signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Pass form data to the success page
            return redirect('signup_success', form_data=form.cleaned_data)
    else:
        form = SignUpForm()
    return render(request, 'momui/momreg.html', {'form': form})

def signup_success(request, form_data):
    return render(request, 'momui/signup_success.html', {'form_data': form_data})
