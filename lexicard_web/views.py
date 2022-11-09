import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth.validators import ASCIIUsernameValidator


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
                    messages.error(request, 'Invalid password')
                    return render(request, self.template_name)
            else:
                messages.error(request, 'Username does not exist')
                return render(request, self.template_name)
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



            # Check if email exists in database
            username_check = User.objects.filter(username=username)
            email_check = User.objects.filter(email=email)
            if username_check.count() > 0:
                messages.error(request, 'Username is already in use.')
                return render(request, self.template_name)
            if email_check.count() > 0:
                messages.error(request, 'Email is already in use.')
                return render(request, self.template_name)

            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request, '<br>'.join(e.messages))
                return render(request, self.template_name)

            user = User(username=username, email=email, password=make_password(password))
            user.save()
            return redirect('/login')
        else:
            print(form.errors)

        return redirect("/register")

class DashboardView(TemplateView):
    """
    Class handler for the main page.

    Allowed methods:
    GET

    """
    template_name = 'dashboard.html'


class ProfileView(View):
    """
    Class handler for user profiles.

    Allowed methods:
    GET

    """

    template_name = None

    def get(self, request):
        pass

class UploadProfileView(View):
    """
    Class handler for uploading/updating user profiles.

    Allowed methods:
    GET POST

    """

    template_name = "pfp.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        # TODO:
        # 1. Implementation of "if image exists", basically checking
        # 2. Implementation of image deletion if user replaces
        #       their profile picture
        # NOTE:
        # 1. Saving image/pfp is working

        image = request.FILES.getlist("image")
        print(image)

        data = Profile(
            user_id=request.user,
            user_image=image[0]
        )
        data.save()


        return redirect("/profile")


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

class FlashcardView(TemplateView):
    """
    Class handler for the available flashcard page.

    Allowed methods:
    GET POST

    """
    template_name = "flashcards.html"


class ProfileView(View):
    """
    Class handler for the available flashcard page.

    Allowed methods:
    GET POST

    """
    def get(self, request):
        template_name = "profile.html"
        return render(request, template_name)
    
    def post(self, request):
        # TODO:
        # 1. Implementation of "if image exists", basically checking
        # 2. Implementation of image deletion if user replaces
        #       their profile picture
        # NOTE:
        # 1. Saving image/pfp is working

        image = request.FILES.getlist("image")
        uname = request.POST.get("username")
        mail = request.POST.get("email")
        
        print(image)

        data = Profile(
            user_id=request.user,
            user_image=image[0]
        )
        data.save()

        p_data = User(
            username=uname,
            email=mail
        )
        p_data.update()

        return redirect("/profile")