from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.hashers import check_password, make_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User


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
            return HttpResponseRedirect(reverse('campusmart:index'))
        else:
            errors = [('Error', "The username/password combination does not match our records.")]

    return render(request, 'campusmart/login.html', {'errors': errors})

def logout(request):
    # remove the logged-in user information
    del request.session["user"]
    return HttpResponseRedirect(reverse("campusmart:login"))