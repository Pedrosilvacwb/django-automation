from django.contrib import auth, messages
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from dataentry.task import celery_test_task

from .forms import RegistrationForm


def home(request: HttpRequest):
    return render(request, "home.html")


def celery_test(request: HttpRequest):
    celery_test_task.delay()
    return HttpResponse("<h1>Task completed successfully!</h1>")


def register(request: HttpRequest):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration succssesful!")
            return redirect("register")
        else:
            context = {"form": form}
        return render(request, "auth/register.html", context)
    else:
        form = RegistrationForm()
        context = {"form": form}
    return render(request, "auth/register.html", context)


def login(request: HttpRequest):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                return redirect("home")
        else:
            messages.error(request, "Invalid Credentials!")
            return redirect("login")
    else:
        form = AuthenticationForm()
        context = {"form": form}

    return render(request, "auth/login.html", context)


def logout(request: HttpRequest):
    auth.logout(request)
    return redirect("home")
