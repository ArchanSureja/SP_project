from django.shortcuts import render, redirect
from django.http import HttpResponse
from authApp.apps import AuthConfig
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from urllib.parse import urlencode
import random
from django.conf import settings
from django.core.mail import send_mail
from note.models import Note
from django.http import HttpResponse,JsonResponse

def home(request):
    return render(request, 'authApp/home.html')


def register(request):
    content = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        cnfrmpassword = request.POST.get('cnfrmpassword')
        email = request.POST.get('email')

        if User.objects.filter(username=username).exists() and password != cnfrmpassword:
            note = 'This username is already taken. Enter a unique username. and Passwords do not match'
            content = { 'msg':note, 'username': request.POST.get('username', ''),'email': request.POST.get('email', '') }

        elif User.objects.filter(username=username).exists():
            content = { 'msg':'This username is already taken. Enter a unique username.', 'username': request.POST.get('username', ''),'email': request.POST.get('email', '') }

        elif password != cnfrmpassword:
            content = {'msg':'Passwords do not match.', 'username': request.POST.get('username', ''),'email': request.POST.get('email', '') }
        
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('/authApp/login')
    
    return render(request, 'authApp/register.html', content)


def login_user(request):
    if request.user.is_authenticated:
        return redirect("/authApp/")
    else:
        if request.method == "POST" :
            username = request.POST['username']
            password = request.POST['password']
            email = request.POST['email']
            user = authenticate(username = username, password = password, email = email)   

            if user is not None:    
                login(request, user)
                return redirect("/authApp/")
            else:
                content = {'msg' : 'Enter valid credentials. User does not match.'}
                return render(request, 'authApp/login.html', content) 
        else:
            return render(request, 'authApp/login.html')
        
def logout_user(request):
    logout(request)
    return redirect('/authApp/login')



def forgotPasswordPage(request):
    return render(request, 'authApp/forgotPassword.html')


def PassForgot(request):
    global check 
    global requestUser
    check = False
    if request.method == 'POST':
        username = request.POST['username']
        if User.objects.filter(username=username).exists():
             check = True
             requestUser = User.objects.get(username=username)
             return redirect('/authApp/resetPasswordPage/')
        else:
            msg = 'Username does not exist.'
            return render(request, 'authApp/forgotPassword.html', {'msg': msg})
    else :
        return render(request, 'authApp/forgotPassword.html')

                  
  
def resetPasswordPage(request):
    global otp 
    if request.method == 'POST':
            otpInput = request.POST['otp']
            passwordNew = request.POST['passwordNew']
            if check :
                user = requestUser
            else:
                user = request.user
            print(otpInput)
            print(otp)
            if  otpInput==str(otp):
                  print("otp matched succesfully")
                  print(user)
                  user.set_password(passwordNew)
                  user.save()
                  logout(request)
                  msg = 'Password successfully updated.'
                  return render(request, 'authApp/resetPassword.html', {'msg': msg})
            else:
                msg = 'otp is incorrect'
                return render(request, 'authApp/resetPassword.html', {'msg': msg})
    else:
         if request.user.is_authenticated or check:
                  otp = random.randint(1000,9999)
                  subject = 'reset password otp'
                  massage = 'your password otp'+ ' '+str(otp)
                  email_from = settings.EMAIL_HOST_USER
                  if check:
                    print(requestUser.email)
                    recipient_email = [requestUser.email]
                  else:
                    print(request.user.email)
                    recipient_email = [request.user.email]

                  send_mail(subject, massage, email_from, recipient_email)
                  print("otp sent successfully")
                  return render(request, 'authApp/resetPassword.html')
         else:
            return redirect('/authApp/login')



class NoteSuggestion:
    def __init__(self, name, id):
        self.name = name
        self.id = id


def note_suggestions(request):
    if request.method == 'GET' and 'search' in request.GET:
        search_term = request.GET.get('search')
        print(search_term)
        notes = Note.objects.filter(title__icontains=search_term,createdBy=request.user)[:10]

        suggestions = []
        for note in notes:
            suggestion = NoteSuggestion(name=note.title, id=note.id)
            suggestions.append(suggestion)

        response_data = {
            'suggestions': [{'name': suggestion.name, 'id': suggestion.id} for suggestion in suggestions]
        }
        return JsonResponse(response_data)
    else:
        return JsonResponse({})   
    

