# Django authentication libraries
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


def login_view(request):
    error_message = None
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("recipes:recipes_list")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    context = {"form": form, "error_message": "Invalid username or password."}
    return render(request, "auth/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request, "You've successfully logged out.")
    return redirect("success")


def about_view(request):
    return render(request, "recipes/about.html")


def list_view(request):
    return render(request, "recipes/recipes_list.html")


def recipes_home(request):
    return render(request, "recipes/recipes_home.html")


def create_view(request):
    return render(request, "recipes/create.html")
