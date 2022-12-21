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
from django.core.mail import send_mail
from django.conf import settings

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
        classes = Classes.objects.filter(
            user_id = request.user.user_id
        )

        context = {
            "flashcard": flashcard,
            "classes" : classes,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        notif = request.POST.get('notifs')
        User.objects.filter(user_id=request.user.user_id).update(notifs = True if notif == "True" else False)
        return redirect('/home/')



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
    def post(self, request):
        notif = request.POST.get('notifs')
        User.objects.filter(user_id=request.user.user_id).update(notifs = True if notif == "True" else False)
        return redirect('/classes/')


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
            "class": class_,
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

class ClassRenameView(View):
    template_name = 'classes-rename.html'

    def get(self, request):
        classes = Classes.objects.filter(user_id = request.user)
        context = { "classes": classes }
        return render(request, self.template_name, context)

    def post(self, request):
        classes_id = request.POST.get("classes_id")
        classes_name = request.POST.get("classes_name")
        class_ = Classes.objects.filter(classes_id = classes_id, user_id = request.user).update(classes_name = classes_name)
        return redirect("/classes/")

class ClassRenamingView(View):
    template_name = 'classes-renaming.html'
    def get(self, request, classes_id):
        classes = Classes.objects.get(classes_id=classes_id)
        context = { "classes" : classes }
        return render(request, self.template_name, context)

    def post(self, request, classes_id):
        classes_name = request.POST.get("classes_name")
        class_ = Classes.objects.filter(classes_id = classes_id, user_id = request.user).update(classes_name = classes_name)
        return redirect("/classes/")

class ClassDeleteView(View):
    template_name = 'classes-delete.html'

    def get(self, request):
        classes = Classes.objects.filter(user_id = request.user)
        context = { "classes": classes }
        return render(request, self.template_name, context)


class ClassDeletingView(View):
    def get(self, request, classes_id):
        if not Classes.objects.filter(classes_id = classes_id, user_id = request.user).exists():
            return redirect('/classes/')
        class_ = Classes.objects.filter(classes_id = classes_id, user_id = request.user).delete()
        return redirect("/classes/")


class NotificationView(View):
    template_name = "header.html"
    def get(self, request):
        # subject = 'FRICK'
        # message = f'Hi {request.user.username}, frick you'
        # email_from = settings.EMAIL_HOST_USER
        # recipient_list = ['graecuskppa@gmail.com', ]
        # send_mail( subject, message, email_from, recipient_list )
        return render(request, self.template_name)

