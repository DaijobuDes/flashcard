from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.exceptions import ValidationError
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View

from .forms import *
from .generate import Generate

# Create your views here.

class DashboardView(View):
    """
    Class handler for the main page.

    Allowed methods:
    GET

    """
    template_name = 'dashboard.html'

    def get(self, request):
        flashcard = Flashcard.objects.filter(
            user_id = request.user.user_id
        )

        context = {
            "flashcard": flashcard,
        }

        return render(request, self.template_name, context)

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

class ScheduleView(TemplateView):
    template_name = "schedules.html"