from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View

from .forms import *
from .generate import Generate

class ScheduleView(View):
    
    template_name = "schedules.html"

    def get(self, request):
        reminders = Reminders.objects.all()
        return render(request, self.template_name, {'reminders':reminders})

def createSched(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        name = request.POST.get("name")
        label = request.POST.get("label")
        date = request.POST.get("date")
        time = request.POST.get("time")
        datetime = date + time

        reminder = Reminders.objects.create(user_id = request.user, reminder_name = name, reminder_label = label, reminder_end_timestamp = datetime)
    return render(request, 'schedule-create.html')