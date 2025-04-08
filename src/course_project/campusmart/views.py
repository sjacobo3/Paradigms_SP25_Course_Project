from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User, Listing
from django.contrib import messages
from datetime import datetime
from django.utils import timezone

# Create your views here.
def index(request):
    context = {
        "course": "CSE-30332",
        "semester": "Spring 2024",
    }
    return render(request, 'campusmart/index.html', context)

# register, login, logout from course repo
# https://stackoverflow.com/a/43793754
def register(request):
    if request.POST:
        # Create a model instance and populate it with data from the request
        name = request.POST["name"]
        uname = request.POST["username"]
        pwd = request.POST["password"]
        email = request.POST["email"]

        user = User(name=name, username=uname, password=pwd, email=email)

        try:
            user.full_clean()
            user.password = make_password(pwd)  # encrypts
            # if we reach here, the validation succeeded
            user.save()  # saves on the db
            # redirect to the login page
            return HttpResponseRedirect(reverse('campusmart:index'))
        except ValidationError as e:
            return render(request, template_name='campusmart/register.html', context={'error_message': e.message_dict})
    return render(request, 'campusmart/register.html')
    
def login(request):
    errors = None
    if request.POST:
        # Create a model instance and populate it with data from the request
        uname = request.POST["username"]
        pwd = request.POST["password"]
        user = User.objects.filter(username=uname)

        if len(user) > 0 and check_password(pwd, user[0].password):
            # create a new session
            request.session["user"] = uname
            return redirect("campusmart:dashboard")  # ✅ redirect here
            # return HttpResponseRedirect(reverse('campusmart:index'))
        else:
            errors = [('Error', "The username/password combination does not match our records.")]

    return render(request, 'campusmart/login.html', {'errors': errors})

def logout(request):
    # remove the logged-in user information
    del request.session["user"]
    return HttpResponseRedirect(reverse("campusmart:login"))

def dashboard(request):
    # Get the username from session
    username = request.session.get("user", None)
    
    # Optional: Get the full user object if needed
    user = User.objects.filter(username=username).first()

    listings = Listing.objects.all()
    return render(request, "campusmart/dashboard.html", {
        "listings": listings,
        "user": user,
    })

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

def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect("dashboard")

    return render(request, "campusmart/delete_listing.html", {"listing": listing})
