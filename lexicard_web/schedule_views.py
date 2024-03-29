import pathlib
from django.db import transaction
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotAllowed, HttpResponseServerError)
from django.shortcuts import redirect, render
from django.views.generic import FormView, TemplateView, View

from django.core.files.storage import FileSystemStorage
from datetime import date, timedelta, datetime
from django.utils.timezone import get_current_timezone, make_aware
from django.core.mail import send_mail
from django.conf import settings


from .forms import *
from .generate import Generate

class ScheduleView(View):
    """
    Class handler for the schedule page.

    - Includes schedule deletion

    Allowed methods:
    GET POST

    """

    template_name = "schedules.html"

    def get(self, request):
        reminders = Reminders.objects.filter(user_id = request.user.user_id).order_by('reminder_timestamp')
        # print(reminders[2].reminder_timestamp)
        context = {
            'reminders': reminders
        }
        return render(request, self.template_name, context)

    # Delete Sched
    def post(self, request, *args, **kwargs):
        reminder_ids = request.POST.getlist('id[]')
        for reminder_id in reminder_ids:
            print(reminder_id)
            try:
                reminder = Reminders.objects.get(reminder_id=reminder_id)
                reminder.delete()
            except Reminders.DoesNotExist:
                reminder = None


        notif = request.POST.get('notifs')
        User.objects.filter(user_id=request.user.user_id).update(notifs = True if notif == "True" else False)
        return redirect("viewAllSched")



# Create Sched
class CreateSchedView(View):
    """
    Class handler for the schedule creation.

    Allowed methods:
    GET POST

    """

    template_name = "schedule-create.html"

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        form = ScheduleForm(request.POST)
        name = request.POST.get("name")
        label = request.POST.get("label")
        date = request.POST.get("date")
        time = request.POST.get("time")
        dt_string = date +" "+ time +":00"
        timedate =  make_aware(datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S"))
        reminder = Reminders.objects.create(user_id = request.user, reminder_name = name, reminder_label = label, reminder_timestamp = timedate)
        reminder.save()
        #return render(request, self.template_name)
        return redirect("viewAllSched")

# Update sched
class UpdateSchedView(View):
    """
    Class handler for the main page.

    Allowed methods:
    GET POST

    """

    def post(self, request):
        id = request.POST.get('id', '')
        type = request.POST.get('type', '')
        value = request.POST.get('value', '')

        rem = Reminders.objects.get(reminder_id=id)

        if type == "date":
            date = value
            time = rem.reminder_timestamp.strftime("%H:%M:%S")
            dt_string = date + " " + time
            timedate =  make_aware(datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S"))
            Reminders.objects.filter(reminder_id=id).update(reminder_timestamp=timedate)
        if type == "time":
            time = value
            date = rem.reminder_timestamp.strftime("%Y-%m-%d")
            dt_string = date + " " + time + ":00"
            timedate = make_aware(datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S"))
            Reminders.objects.filter(reminder_id=id).update(reminder_timestamp=timedate)
        if type == "name":
            name = value
            Reminders.objects.filter(reminder_id=id).update(reminder_name=name)
        if type == "details":
            details = value
            Reminders.objects.filter(reminder_id=id).update(reminder_label=details)

        return redirect("viewAllSched")

