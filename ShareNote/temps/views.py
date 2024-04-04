
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def view_temps(request):
    return render(request, "temps/view_temps.html")

@login_required
def daily_schedule(request):
    return render(request, "temps/Daily_Schedule.html")

@login_required
def week_schedule(request):
    return render(request, "temps/week_Schedule.html")

@login_required
def todo(request):
    return render(request, "temps/To_Do.html")
