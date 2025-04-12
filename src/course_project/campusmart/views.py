from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Listing, Conversation, ConversationMessage
from django.contrib import messages
from django.utils import timezone
from django.contrib.auth import authenticate as authenticate_user, login as login_user, logout as logout_user
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
def index(request):
    ''' This function displays the landing page (index.html). '''
    return render(request, 'campusmart/index.html')

def register(request):
    ''' This function implements Feature 1.1: Create New User Profile '''
    # if user is already logged in, reroute them to the listing page
    if request.user.is_authenticated:
        messages.error(request, f'You are already logged in as {request.user.username}. Logout first to switch account.')
        return HttpResponseRedirect(reverse('campusmart:listing_all'))
    
    # retrieve data from the user's submission
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        username = request.POST["username"]
        password = request.POST["password"]

        # error check: ensure all fields were filled in as well as unique username and email
        if not name or not username or not password or not email:
            messages.error(request, "Name, Username, Password, and Email are required.")
            return HttpResponseRedirect(reverse('campusmart:register'))
        if User.objects.filter(email=email).exists():
            messages.error(request, f'Email {email} is already in use.')
            return HttpResponseRedirect(reverse('campusmart:register'))
        
        try:
            # create the user with the django built-in model
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = name # first_name acts as the full name, as per edstem question
            user.save()

            # automatically log the user in after registration and redirect to listing page
            login_user(request, user)
            return HttpResponseRedirect(reverse('campusmart:listing_all'))
        # error check: return error messages and redirect to register again
        except ValidationError as ve:
            messages.error(request, ve.message_dict)
            return HttpResponseRedirect(reverse('campusmart:register'))
        except Exception as e:
            messages.error(request, str(e))
            return HttpResponseRedirect(reverse('campusmart:register'))

    return render(request, 'campusmart/register.html')


def login(request):
    if request.user.is_authenticated:
        messages.error(request, f'You are already logged in as {request.user.username}. Logout first to switch account.')
        return HttpResponseRedirect(reverse('campusmart:listing_all'))
    errors = None
    if request.method == "POST":
        uname = request.POST["username"]
        pwd = request.POST["password"]
        user = authenticate_user(request, username=uname, password=pwd)

        if user is not None:
            login_user(request, user)  
            return HttpResponseRedirect(reverse('campusmart:listing_all'))  
        else:
            messages.error(request, "The username/password combination does not match our records.")
    return render(request, 'campusmart/login.html')


def logout(request):
    # remove the logged-in user information
    logout_user(request)
    return HttpResponseRedirect(reverse("campusmart:index"))


@login_required
def create_listing(request):
    ''' This function implements Feature 2.1: Create Listings '''
    # retrieve data from the user's listing
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        price = request.POST.get("price")
        condition = request.POST.get("condition")
        photo = request.FILES.get("photo")  

        # check for missing fields
        if not all([title, description, price, condition, photo]):
            messages.error(request, "All fields are required.")
            return redirect("campusmart:create_listing")  

        # check if price is valid
        try:
            price = float(price)
        except ValueError:
            messages.error(request, "Provide a valid price.")
            return redirect("campusmart:create_listing")

        # reset daily counter
        last_post_date = request.session.get("last_post_date")
        today_str = timezone.now().strftime("%Y-%m-%d")

        if last_post_date != today_str:
            request.session["daily_post_count"] = 0
            request.session["last_post_date"] = today_str
       
        # check posting limit
        daily_post_count = request.session.get("daily_post_count", 0)
        if daily_post_count >= 3:
            messages.error(request, "You have reached your daily limit of 3 listings.")
            return redirect("campusmart:listing_all")      # can redirect to buy more listing posts

        # if all fields are filled, save the listing
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

        # update session tracking
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
            messages.error(request, "Provide a valid price.")
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
    ''' This function implements Feature 3.1 View all listings '''
    # set initial variables, set up pagination for 20 products at a time
    page = int(request.GET.get('page', 1))
    per_page = 20
    start = (page-1) * per_page
    end = start + per_page

    query = request.GET.get('query', '') # used later for Feature 3.2
    if query:
        listings = Listing.objects.filter(description__icontains=query)
    else:
            listings = Listing.objects.filter(status='Available') # this is Feature 3.1, showing all available listings
   
    page_listings = listings[start:end]
    total = listings.count()
    total_pages = (total + per_page - 1) // per_page  # round up to get number of pages

    page_range = range(1, total_pages + 1)

    # display listings page
    return render(request, 'campusmart/listing_all.html', {
        'query': query,
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


@login_required
def conversation_new(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)

    # check if conversation exists
    conversations = Conversation.objects.filter(listing=listing).filter(members__in=[request.user.id])
    if conversations:
        return redirect('campusmart:inbox')      # redirect to messages page

    # create conversation, if none exist
    if request.method == 'POST':
        new_conversation = Conversation.objects.create(listing=listing)
        new_conversation.members.add(request.user)
        new_conversation.members.add(listing.created_by)

        # create message        
        message_content = request.POST.get('message')
        if message_content:
            new_message = ConversationMessage.objects.create(
                conversation=new_conversation,
                content=message_content,
                created_by=request.user,
            )
            new_message.save()

        # redirect to inbox after sending message
        return redirect('campusmart:inbox')

    return render(request, 'campusmart/conversation_new.html', {
        'listing':listing,
    })


@login_required
def conversation_detail(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # get all messages for conversation
    messages = ConversationMessage.objects.filter(conversation=conversation).order_by('created_at')

    # if user sends message in conversation_detail
    if request.method == 'POST':
        message_content = request.POST.get('message')
        if message_content:
            new_message = ConversationMessage.objects.create(
                conversation=conversation,
                content=message_content,
                created_by=request.user,
            )
            new_message.save()
            return redirect('campusmart:conversation_detail', conversation_id=conversation.id)

    return render(request, 'campusmart/conversation_detail.html', {
        'conversation':conversation,
        'messages':messages,
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    
    return render(request, 'campusmart/inbox.html', {
        'conversations':conversations,
    })
