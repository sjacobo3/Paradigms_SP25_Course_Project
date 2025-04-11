from django.contrib.auth.models import User
from django.contrib.auth import authenticate as authenticate_user, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Listing
from django.contrib import messages
from django.utils import timezone

# Create your views here.
def index(request):
    return render(request, 'campusmart/index.html')

def register(request):
    if request.user.is_authenticated:
        messages.error(request, f'You are already logged in as {request.user.first_name}. Logout first to switch account.')
        return HttpResponseRedirect(reverse('campusmart:dashboard'))
    if request.POST:
        # populate the built-in User model with data from the request
        name = request.POST["name"]
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]

        if not name or not username or not password or not email:
            messages.error(request, "Name, Username, Password, and Email are required.")
            return redirect("register")

        try:
            user = User.objects.create_user(username, email, password) # encrypts the password as well
            user.first_name = name
            user.full_clean()
            # if we reach here, the validation succeeded
            user.save()  # saves on the db
            # redirect to the dashboard
            return HttpResponseRedirect(reverse('campusmart:dashboard'))
        except ValidationError as ve:
            messages.error(request, ve.message_dict)
            return HttpResponseRedirect(reverse('campusmart:register'))
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect(reverse('campusmart:register'))
    return render(request, 'campusmart/register.html')
    
def login(request):
    if request.user.is_authenticated:
        messages.error(request, f'You are already logged in as {request.user.first_name}. Logout first to switch account.')
        return HttpResponseRedirect(reverse('campusmart:dashboard'))
    errors = None
    if request.POST:
        # Create a model instance and populate it with data from the request
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate_user(request, username=username, password=password)

        if user is not None:
            login_user(request, user)
            return HttpResponseRedirect(reverse('campusmart:dashboard'))
        else:
            errors = [('Error', "The username/password combination does not match our records.")]

    return render(request, 'campusmart/login.html', {'errors': errors})

def logout(request):
    logout_user(request)
    return HttpResponseRedirect(reverse("campusmart:index"))

@login_required
def dashboard(request):
    listings = Listing.objects.all()
    return render(request, "campusmart/dashboard.html", {
        "listings": listings,
        # "user": user,
    })

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description") 
        price = request.POST.get("price") 
        condition = request.POST.get("condition") 
        photo = request.FILES.get("photo")  

        # Check for missing fields
        if not title or not description or not price or not condition or not photo:
            messages.error(request, "All fields are required.")
            return redirect("create_listing")  

        # Reset daily counter
        last_post_date = request.session.get("last_post_date")
        today_str = timezone.now().strftime("%Y-%m-%d")

        if last_post_date != today_str:
            request.session["daily_post_count"] = 0
            request.session["last_post_date"] = today_str
        
        # Check posting limit
        daily_post_count = request.session.get("daily_post_count", 0)
        if daily_post_count >= 3:
            messages.error(request, "You have reached your daily limit of 3 listings.")
            return redirect("dashboard")

        # If all fields are filled, save the listing
        listing = Listing(
            title=title,
            description=description,
            price=price,
            condition=condition,
            photo=photo,
            status="Available",  # default status
        )
        listing.save()  # save the new listing

        # Update session tracking
        request.session["daily_post_count"] = daily_post_count + 1
        request.session["last_post_date"] = today_str

        messages.success(request, "Your listing has been posted successfully :)")
        return redirect("dashboard")  # redirect to a dashboard or listing page

    return render(request, "campusmart/create_listing.html")

@login_required   
def update_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description") 
        price = request.POST.get("price") 
        condition = request.POST.get("condition") 
        status = request.POST.get("status")
        photo = request.FILES.get("photo")   

        # Validate fields
        if not all([title, description, price, condition, status]):
            messages.error(request, "All fields are required.")
            return redirect("update_listing", listing_id=listing_id)

        # Update fields
        listing.title = title
        listing.description = description
        listing.price = price
        listing.condition = condition
        listing.status = status
        if photo:
            listing.photo = photo
        listing.save()

        messages.success(request, "Listing updated successfully!")
        return redirect("dashboard")

    return render(request, "campusmart/update_listing.html", {"listing": listing})

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect("dashboard")

    return render(request, "campusmart/delete_listing.html", {"listing": listing})
