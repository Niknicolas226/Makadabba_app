from time import sleep
import time
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
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import PasswordResetTokenGenerator




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

class TokenGenerator(PasswordResetTokenGenerator):
    pass

generate_token = TokenGenerator()

def home_signup(request):
    
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        if User.objects.filter(username=username).exists():
            message = "Username already exists! Please try some other username."
            return render(request, 'signup_error.html', {'message': message})

        if User.objects.filter(email=email).exists():
            message = "Email already exists! Please use a different email."
            return render(request, 'signup_error.html', {'message': message})

        if len(username) > 20:
            message = "Username must be under 20 characters!!"
            return render(request, 'signup_error.html', {'message': message})

        if pass1 != pass2:
            message = "Passwords didn't match!!"
            return render(request, 'signup_error.html', {'message': message})

        if not username.isalnum():
            message = "Username must be Alpha-Numeric!!"
            return render(request, 'signup_error.html', {'message': message})

        
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        # myuser.is_active = False
        myuser.is_active = False
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check your email to confirm your email address in order to activate your account.")
        
        # Welcome Email
        subject = "Welcome to MA KA DABBA!!"
        message = f"Hello {myuser.first_name}!!\n\nWelcome to Ma Ka Dabba Restaurant!\n\nThank you for visiting our website. We're thrilled to have you join our community of food enthusiasts who appreciate home-cooked goodness delivered straight to their doorstep.\n\nWe've received your order and want to ensure that everything is perfect for you. To confirm your email address and complete the registration process, please click on the confirmation link we've sent to your inbox.\n\nIf you don't see the email in your inbox, please check your spam or junk folder just in case it got misplaced.\n\nWe're excited to have you as part of the Ma Ka Dabba family! If you have any questions or need further assistance, feel free to reach out to us.\n\nThanking You,\nAditya Tamta\nMa Ka Dabba Restaurant"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        
        # Email Address Confirmation Email
        current_site = get_current_site(request)
        email_subject = "Confirm your Email Ma ka dabba LOGIN"
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
        email.content_subtype = "html"  # Set the content type to HTML
        messages.info(request, "Email is sending, please wait.")
            
            # Simulate email sending delay

        
        messages.success(request, "Confirmation email sent. Please check your inbox.")
    
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
    


@login_required
def payment_gateway(request):
    # Get the cart for the current user
    cart = get_object_or_404(Cart, user=request.user)
    
    # Get the cart items for the current user's cart using the 'items' related name
    cart_items = cart.items.all()
    
    # Calculate the total amount for the cart items
    total_amount = sum(item.total_price for item in cart_items)
    
    # Initialize a PaymentForm instance
    payment_form = PaymentForm()
    
    # Process the form if it's submitted
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            # Process the payment based on the selected payment method
            selected_payment_method = payment_form.cleaned_data['payment_method']
            if selected_payment_method == 'cash':
                # Implement your logic for cash payment here
                # For example, you can redirect to a confirmation page
                return redirect('payment_confirmation')
            elif selected_payment_method == 'online':
                # Implement your logic for online payment here
                # For example, you can integrate with a payment gateway API
                # After successful payment, redirect to a confirmation page
                return redirect('payment_confirmation')
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'payment_form': payment_form,
    }
    
    return render(request, 'payment_gateway.html', context)

@login_required
def process_payment(request):
    # Implement your payment processing logic here
    # For example, you can integrate with a payment gateway API to process the payment
    # After successful payment, you can redirect to a confirmation page
    return redirect('process_payment.html')