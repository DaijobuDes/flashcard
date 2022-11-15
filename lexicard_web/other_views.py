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

class ClassesView(View):
    template_name = 'classes.html'
    def get(self, request):
        classes = Classes.objects.filter(
            user_id = request.user.user_id
        )

        context = {
            "class": classes,
            "flag" : classes.count(),
        }

        return render(request, self.template_name, context)


class ClassView(View):
    """
    Class handler for the available classes page.

    Allowed methods:
    GET POST

    """
    template_name = "class_view.html"
    def get(self, request, classes_id):
        if not Classes.objects.filter(classes_id = classes_id).exists():
            return redirect('/home/')
        class_ = Classes.objects.get(classes_id=classes_id)
        decks = class_.deck_set.all()
        context = {
            "decks": decks,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        pass

class ClassCreateView(View):
    template_name = 'class_create.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        class_name = request.POST.get("class_name")
        class_ = Classes(classes_name = class_name, user_id = request.user)
        class_.save()
        return redirect("/classes/")









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