import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View

from .forms import *

# Create your views here.

class Login(FormView):
    """
    Class handler for logging in users.

    Allowed HTTP methods:
    GET POST
    """

    form_class = UserForm
    template_name = None

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = UserForm(request.POST)

        if form.is_valid():
            email = request.POST.get("email")
            password = request.POST.get("password")

            # Check if email exists
            if User.objects.filter(email=email).exists():
                user = authenticate(email=email, password=password)
                if user is not None:
                    user.save()
                    login(request, user)
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
                        "message": "Email does not exist."
                    }
                ))
        return render(request, self.template_name)


class Logout(View):
    """
    Class handler for logging out users.

    Allowed methods:
    GET
    """

    template_name = None

    def get(self, request):
        logout(request)
        return redirect("/")

    def post(self, request):
        return HttpResponseNotAllowed(["GET"])


class Register(FormView):
    """
    Class handler for user registration.

    Allowed methods:
    GET POST
    """

    form_class = RegistrationForm
    template_name = "register.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            email = request.POST.get("email")
            password = request.POST.get("password")

            # Check if email exists in database
            username_check = User.objects.filter(username=username)
            email_check = User.objects.filter(email=email)
            if username_check > 0 or email_check > 0:
                return HttpResponseBadRequest(json.dumps(
                    {
                        "status": "error",
                        "code": "400",
                        "message": "Email/username is taken."
                    }
                ))

            try:
                validate_password(password=password)
            except ValidationError as ve:
                return HttpResponseBadRequest(json.dumps(
                    {
                        "status": "error",
                        "code": "400",
                        "message": "Email/username is taken."
                    }
                ))

            user = User(
                username=username,
                email=email,
                password=make_password(password)
            )

            login(request, user)

        return redirect("/login")

