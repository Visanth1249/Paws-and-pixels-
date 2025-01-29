from django.shortcuts import render, redirect
from .models import UserRegistration, Accessory, Adoption
from .forms import UserRegForm, LoginForm,AdoptionForm,AccessoryForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import CartItem, Order

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem, Accessory

from django.shortcuts import get_object_or_404, redirect
from .models import Cart, Accessory



def order_success(request):
    return render(request, 'order_success.html', {'message': 'Your order was successful!'})

from django.http import JsonResponse

@login_required
def add_to_cart(request, accessory_id):
    accessory = get_object_or_404(Accessory, id=accessory_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, accessory=accessory)

    if not item_created:
        cart_item.quantity += 1
        cart_item.save()

    # Get updated cart count
    cart_count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))

    return JsonResponse({"cart_count": cart_count})

@login_required
def get_cart_count(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_count = sum(item.quantity for item in CartItem.objects.filter(cart=cart))
    return JsonResponse({"cart_count": cart_count})


from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from .models import Adoption
from django.contrib import messages

def adopt_pet(request, pet_id):
    pet = get_object_or_404(Adoption, id=pet_id)

    if request.method == "POST":
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        address = request.POST.get("address")

        # Mark pet as adopted
        pet.available = False
        pet.save()

        # Send confirmation email
        subject = "Adoption Confirmation - Paws and Pixels"
        message = f"Congratulations! You have successfully adopted {pet.animal_name}.\n\n"
        message += "Please visit the shelter to take your pet home.\n\n"
        message += f"Pet Name: {pet.animal_name}\nType: {pet.animal_type}\n\n"
        message += "Thank you for adopting and giving a pet a loving home!"

        send_mail(subject, message, "your-email@example.com", [email], fail_silently=False)

        messages.success(request, "Adoption successful! Check your email for confirmation.")
        return redirect("adoptions")

    return render(request, "adoption_form.html", {"pet": pet})


@login_required
def view_cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total price
    total_price = sum(item.accessory.price * item.quantity for item in cart_items)

    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import CartItem, Order  # Assuming you have CartItem and Order models
from django.core.mail import send_mail
from django.conf import settings
from .models import Cart, CartItem, Order

def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)  # Get user's cart
    cart_items = CartItem.objects.filter(cart=cart)  # Fetch items linked to that cart
    total_price = sum(item.accessory.price * item.quantity for item in cart_items)  # Calculate total

    if request.method == "POST":
        email = request.POST.get("email")

        if not cart_items.exists():  # Prevent checkout if cart is empty
            messages.error(request, "Your cart is empty.")
            return redirect("view_cart")

        # Create an order entry
        order = Order.objects.create(user=request.user, email=email, total_price=total_price)

        # Generate bill details
        bill_content = "Your Order Details:\n\n"
        for item in cart_items:
            bill_content += f"{item.accessory.name} - {item.quantity} x ${item.accessory.price} = ${item.accessory.price * item.quantity}\n"
        bill_content += f"\nTotal Amount: ${total_price}"

        # Send the email
        send_mail(
            subject="Your Order Confirmation - Paws and Pixels",
            message=bill_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        # ✅ Clear the cart after successful checkout
        cart_items.delete()  # Delete all items from the cart
        cart.delete()  # Remove the cart itself

        return redirect("order_success")  # Redirect to a success page

    return render(request, "checkout.html", {"total_price": total_price, "cart_items": cart_items})

@login_required
def increase_cart_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('view_cart')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('view_cart')

@login_required
def add_adoption(request):
    if request.method == 'POST':
        form = AdoptionForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save the adoption to the database
            return redirect('adoptions')  # Redirect to the adoptions list page
    else:
        form = AdoptionForm()
    return render(request, 'Add adoptions.html', {'form': form})



@login_required
def add_accessory(request):
    if request.method == 'POST':
        form = AccessoryForm(request.POST, request.FILES)  # Handle file uploads
        if form.is_valid():
            form.save()  # Save the accessory to the database
            return redirect('accessories')  # Redirect to the accessories list page
    else:
        form = AccessoryForm()
    return render(request, 'Add_accessory.html', {'form': form})


def home(request):
    """
    Home view that displays login, register, and contact links for unauthenticated users.
    Authenticated users will see restricted content.
    """
    return render(request, 'home.html')

def about(request):
    """
    About page view, accessible only to authenticated users.
    Redirects unauthenticated users to the restricted page.
    """
    if not request.user.is_authenticated:
        return redirect('restricted_page')
    return render(request, 'about.html')


def login_view(request):
    """
    Handles user authentication and login.
    """
    if request.user.is_authenticated:
        return redirect('loginsuccess')  # Redirect already logged-in users

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('loginsuccess')  # Redirect to the logged-in success page
            else:
                messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def register(request):
    """
    Handles user registration and creates a new user.
    """
    if request.user.is_authenticated:
        return redirect('loginsuccess')  # Redirect already logged-in users

    if request.method == 'POST':
        form = UserRegForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            # Use set_password to hash the password before saving
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Your account has been created successfully! Please log in.")
            return redirect('login')
        else:
            messages.error(request, "There was an error in the registration form. Please check your input.")
    else:
        form = UserRegForm()

    return render(request, 'register.html', {'form': form})


def loginsuccess(request):
    """
    Displays the post-login success page.
    """
    return render(request, 'loginsuccess.html')

from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect("contact")

        # Email Details
        subject = f"New Contact Form Submission from {name}"
        email_message = f"You received a new message from {name} ({email}):\n\n{message}"
        admin_email = "your-email@example.com"  # Change to your email

        # Send email from user's email
        send_mail(subject, email_message, email, [admin_email], fail_silently=False)

        messages.success(request, "Message sent successfully. We'll get back to you soon!")
        return redirect("contact")

    return render(request, "contactus.html")

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

def feedback_view(request):
    if request.method == 'POST':
        feedback = request.POST.get('feedback')

        # Send email with feedback content
        send_mail(
            'New Feedback Submitted',  # Subject
            feedback,  # Message
            settings.DEFAULT_FROM_EMAIL,  # From Email (default email in settings)
            ['your-email@example.com'],  # To Email (where feedback will be sent)
            fail_silently=False,
        )

        return render(request, 'feedback_thank_you.html')  # Redirect to a custom thank-you page

    return render(request, 'feedback.html')  # Render the feedback form if GET request

def contactus(request):
    """
    Contact Us page view.
    """
    return render(request, 'contactus.html')

def accessories(request):
    accessories = Accessory.objects.all()  # Fetch all accessories
    return render(request, 'accessories.html', {'accessories': accessories})

def adoptions(request):
    adoptions = Adoption.objects.all()  # Fetch all pets available for adoption
    return render(request, 'adoptions.html', {'adoptions': adoptions})


@login_required
def feedback(request):
    """
    Feedback page, accessible only to authenticated users.
    """
    return render(request, 'feedback.html')

def submit_feedback(request):
    """
    Handles feedback submission and redirects to the feedback page.
    """
    if request.method == 'POST':
        feedback_text = request.POST.get('feedback')
        # Save feedback logic here (if needed)
        return redirect('feedback')

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

def concern(request):
    if request.method == 'POST':
        concern = request.POST.get('concern')

        # Send email with concern content
        send_mail(
            'New Concern Raised',  # Subject
            concern,  # Message
            settings.DEFAULT_FROM_EMAIL,  # From Email (default email in settings)
            ['your-email@example.com'],  # To Email (where concern will be sent)
            fail_silently=False,
        )

        # Redirect to the 'sorry for the inconvenience' page after submission
        return render(request, 'concern_thank_you.html')

    return render(request, 'concern.html')  # Render the concern form if GET request


def submit_concern(request):
    """
    Handles feedback submission and redirects to the feedback page.
    """
    if request.method == 'POST':
        feedback_text = request.POST.get('concern')
        # Save feedback logic here (if needed)
        return redirect('concern')

def restricted_page(request):
    """
    Restricted page view, displayed to users trying to access unauthorized content.
    """
    return render(request, 'restricted_page.html')

def logout_view(request):
    """
    Logout view that logs out the user and redirects to the home page.
    """
    logout(request)
    return redirect('home')
