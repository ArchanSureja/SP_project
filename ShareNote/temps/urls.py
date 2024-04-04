
from django.urls import path
from . import views 
app_name="temps"
urlpatterns = [
    path("", views.view_temps, name="view_temps"),
    path("daily_schedule/", views.daily_schedule, name="daily_schedule"),
    path("week_schedule/", views.week_schedule, name="week_schedule"),
    path("todo/", views.todo, name="todo"),
]

