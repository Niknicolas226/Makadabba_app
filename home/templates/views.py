from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from pilot import settings
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_str,force_bytes
from django.contrib.auth import authenticate, login, logout
from . tokens import generate_token
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .models import Meal, MenuItem , Cart, CartItem, MenuOption
from .models import Profile
from .forms import ProfileForm, PaymentForm




@login_required
def userui(request):
    menu_options = MenuOption.objects.all()
    return render(request, 'user/index.html', {'menu_options': menu_options})

@login_required
def menuweek(request):
    menu_options = MenuOption.objects.all()
    return render(request, 'user/index.html', {'menu_options': menu_options})


@login_required
def profile(request):
    # Only authenticated users can access this view
    # Add your logic here to display the user profile page
    return render(request, 'profile.html')

def payment_gateway(request):
    return render(request, 'payment_gateway.html') 


# Create your views here.
def home(request):
    return render(request, "home.html")
def momreg(request):
    return render(request, "momregis.html")
def subscription(request):
    return render(request, "monthly.html")



def menu(request):
    breakfast_items = MenuItem.objects.filter(meal__name='Breakfast')
    lunch_items = MenuItem.objects.filter(meal__name='Lunch')
    dinner_items = MenuItem.objects.filter(meal__name='Dinner')

    return render(request, 'menu.html', {
        'breakfast_items': breakfast_items,
        'lunch_items': lunch_items,
        'dinner_items': dinner_items,
    })


@login_required
def custom_login(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('view_cart')
    elif not request.path.startswith('/accounts/signup/'):
        return redirect('signup')  # Assuming 'signup' is the name of your signup page URL
    else:
        return login(request, *args, **kwargs)



@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    total_price = sum(item.total_price for item in cart_items)
    return render(request, 'view_cart.html', {'cart': cart, 'cart_items': cart_items, 'total_price': total_price})

@login_required
def add_to_cart(request, menu_item_id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    menu_item = get_object_or_404(MenuItem, id=menu_item_id)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, menu_item=menu_item)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return JsonResponse({'message': f'{menu_item.name} added to cart'})

@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()
    return redirect('view_cart')


def home_signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return redirect('home')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return redirect('home')
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, "Passwords didn't matched!!")
            return redirect('home')
        
        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric!!")
            return redirect('home')
        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to GFG- Django Login!!"
        message = "Hello " + myuser.first_name + "!! \n" + "Welcome to GFG!! \nThank you for visiting our website\n. We have also sent you a confirmation email, please confirm your email address. \n\nThanking You\n ADITYA TAMTA"        
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email @ GFG - Django Login!!"
        message2 = render_to_string('email_confirmation.html',{
            
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
        email_subject,
        message2,
        settings.EMAIL_HOST_USER,
        [myuser.email],
        )
        email.fail_silently = True
        email.send()
    
    
    return render(request, "signup.html") 
     #return redirect('signin')
        
        



def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except (TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active = True
        # user.profile.signup_confirmation = True
        myuser.save()
        login(request,myuser)
        messages.success(request, "Your Account has been activated!!")
        return redirect('signin.html')
    else:
        return render(request,'activation_failed.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            fname = user.first_name
            messages.success(request, "Logged In Sucessfully!!")
            return render(request, "user/index.html",{"fname":fname})
        else:
            messages.error(request, "Bad Credentials!!")
            return redirect('user/index.html')
    
    return render(request, "signin.html")


def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')
 

@login_required
def view_profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'user/view_profile.html', {'profile': profile})

@login_required
def edit_profile(request):
    user = request.user
    try:
        profile = Profile.objects.get(user=user)
    except Profile.DoesNotExist:
        profile = Profile(user=user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('view_profile')
    else:
        form = ProfileForm(instance=profile)
    

