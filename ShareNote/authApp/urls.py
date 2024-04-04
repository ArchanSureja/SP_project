from django.urls import path
from . import views 
app_name="authApp"
urlpatterns = [
    path("",views.home,name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("resetPasswordPage/", views.resetPasswordPage, name="resetPasswordPage"),
    path('forgotPasswordPage/', views.forgotPasswordPage, name="forgotPasswordPage"),
    path('passFortgot/', views.PassForgot, name="passForgot"),
   path('note-suggestions/', views.note_suggestions, name='note_suggestions'),
]