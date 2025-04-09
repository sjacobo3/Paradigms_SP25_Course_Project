from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Listing
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.contrib.auth import authenticate, login as django_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    context = {
        "course": "CSE-30332",
        "semester": "Spring 2024",
    }
    return render(request, 'campusmart/index.html', context)

def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]

        # Create user
        try:
            # create the user with the built-in model
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            # automatically log the user in after registration
            django_login(request, user)
            
            # Redirect to dashboard after successful registration
            messages.success(request, "Registration successful! You are now logged in.")
            return redirect('campusmart:listing_all')  # Or wherever you want the user to go after logging in
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('campusmart:register')

    return render(request, 'campusmart/register.html')    

def login(request):
    errors = None
    if request.method == "POST":
        uname = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate(request, username=uname, password=pwd)

        if user is not None:
            django_login(request, user)  # django's built-in login function
            return redirect("campusmart:listing_all")  # redirect to the dashboard or wherever appropriate
        else:
            errors = [('Error', "The username/password combination does not match our records.")]
            messages.error(request, "Invalid username or password.")

    return render(request, 'campusmart/login.html', {'errors': errors})

def logout(request):
    # remove the logged-in user information
    auth_logout(request)
    return HttpResponseRedirect(reverse("campusmart:login"))

@login_required
def create_listing(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description") 
        price = request.POST.get("price") 
        condition = request.POST.get("condition") 
        photo = request.FILES.get("photo")  

        # Check for missing fields
        if not all([title, description, price, condition, photo]):
            messages.error(request, "All fields are required.")
            return redirect("campusmart:create_listing")  

        # check if price is valid
        try:
            price = float(price)
        except ValueError:
            message.error(request, "Provide a valid price.")
            return redirect("campusmart:create_listing")

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
            return redirect("campusmart:listing_all")      # can redirect to buy more listing posts

        # If all fields are filled, save the listing
        listing = Listing(
            created_by=request.user,
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
        return redirect("campusmart:listing_all")  # redirect to listing page

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
            return redirect("campusmart:update_listing", listing_id=listing_id)
        
        # check if price is valid
        try:
            price = float(price)
        except ValueError:
            message.error(request, "Provide a valid price.")
            return redirect("campusmart:update_listing", listing_id=listing_id)

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
        return redirect("campusmart:listing_all")

    return render(request, "campusmart/update_listing.html", {"listing": listing})

@login_required
def delete_listing(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    if request.method == "POST":
        listing.delete()
        messages.success(request, "Listing deleted successfully.")
        return redirect("campusmart:listing_all")

    return render(request, "campusmart/delete_listing.html", {"listing": listing})

def listing_all(request):
    page = int(request.GET.get('page', 1))      # default page 1
    per_page = 20
    start = (page-1) * per_page
    end = start + per_page
    
    listings = Listing.objects.filter(status='Available')
    page_listings = listings[start:end]
    total = listings.count()
    total_pages = (total + per_page - 1) // per_page  # round up to get number of pages

    page_range = range(1, total_pages + 1)

    return render(request, 'campusmart/listing_all.html', {
        'listings':page_listings,
        'page':page,
        'total_pages':total_pages,
        'page_range':page_range,
        })

def detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, 'campusmart/listing_detail.html', {
        'listing':listing,
    })