from django.shortcuts import render, redirect
from .forms import QueryForm
# views.py

from django.shortcuts import render

def pricing_view(request):
    # Your pricing view logic here
    return render(request, 'pricing.html')

def settings_view(request):
    # Your settings view logic here
    return render(request, 'settings.html')

def customer_care_view(request):
    # Your customer care view logic here
    return render(request, 'contact.html')

def delivery_view(request):
    # Your delivery view logic here
    return render(request, 'delivery.html')



def submit_query(request):
    if request.method == 'POST':
        form = QueryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('query_success')
    else:
        form = QueryForm()
    return render(request, 'query_form.html', {'form': form})

def query_success(request):
    return render(request, 'query_success.html')



def our_commitment(request):
    return render(request, 'our_commitment.html')

# Create your views here.
