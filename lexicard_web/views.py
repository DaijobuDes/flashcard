import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View
from django.contrib import messages


from .forms import *

# Create your views here.

class Login(FormView):
    """
    Class handler for logging in users.

    Allowed HTTP methods:
    GET POST
    """

    form_class = LoginForm
    template_name = 'login.html'

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            print(password)
            # Check if email exists
            if User.objects.filter(username=username).exists():
                user = authenticate(username=username, password=password)
                print(user)
                if user is not None:
                    user.save()
                    login(request, user)
                    return redirect("/home")
                else:
                    return HttpResponseBadRequest(json.dumps(
                        {
                            "status": "error",
                            "code": "400",
                            "message": "Invalid password."
                        }
                    ))
            else:
                return HttpResponseBadRequest(json.dumps(
                    {
                        "status": "error",
                        "code": "400",
                        "message": "Username does not exist."
                    }
                ))
        else:
            messages.error(request, form.errors)
        return render(request, self.template_name)


class Logout(View):
    """
    Class handler for logging out users.

    Allowed methods:
    GET
    """

    def get(self, request):
        logout(request)
        return redirect("/login/")


class Register(FormView):
    """
    Class handler for user registration.

    Allowed methods:
    GET POST
    """

    form_class = UserForm
    template_name = "register.html"

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")
            print("a")
            # Check if email exists in database
            username_check = User.objects.filter(username=username)
            email_check = User.objects.filter(email=email)
            if username_check.count() > 0:
                messages.error(request, 'Username is already in use.')
                return render(request, self.template_name)
            if email_check.count() > 0:
                messages.error(request, 'Email is already in use.')
                return render(request, self.template_name)

            user = User(
                username=username,
                email=email,
                password=make_password(password)
            )
            user.save()
            return redirect('/login')
        else:
            print(form.errors)

        return redirect("/register")

class DashboardView(View):
    """
    Class handler for the main page.

    Allowed methods:
    GET

    """

    template_name = None

    def get(self, request):
        pass


class ProfileView(View):
    """
    Class handler for user profiles.

    Allowed methods:
    GET

    """

    template_name = None

    def get(self, request):
        pass


class ClassView(View):
    """
    Class handler for the available classes page.

    Allowed methods:
    GET POST

    """

    template_name = None

    def get(self, request):
        pass

    def post(self, request):
        pass

class Document(View):
    """
    Class handler for the main page.

    Allowed methods:
    GET

    """

    template_name = None

    def get(self, request):
        pass
