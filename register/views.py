from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from register.forms import RegisterForm
from django.views.decorators.csrf import csrf_protect, requires_csrf_token

@csrf_protect
def register_user(request):
    if request.method == 'POST':
        ## get user form, and check validity
        form = RegisterForm(request.POST)
        if form.is_valid():
            ## save user, and redirect user to login page
            user = form.save()
            return redirect("login")

        ## form was invalid, return error message
        messages.error(request, "Invalid information. Are you sure you've input everything correctly?")

    ## pass in empty registration form
    form = RegisterForm()
    return render(request, "register/register.html", {"register_user": form})

@csrf_protect
def login_user(request):
    if request.method == "POST":
        ## get auth form, and check validity
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            ## get login details and authenticate user exists
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username, password = password)
            if user is not None: ## user is valid/exists
                login(request, user)
                messages.info(request, f"You are now logged in as {username}")
                return HttpResponseRedirect("/home")
            else:
                messages.error(request, "Invalid username or password")
        else:
            messages.error(request, "Invalid username or password")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"login_user": form})

def logout_user(request):
    logout(request)
    messages.info(request, "You have logged out successfully.")
    return redirect("home")
