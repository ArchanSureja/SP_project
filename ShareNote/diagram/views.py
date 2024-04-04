from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from authApp.apps import AuthConfig
from django.contrib.auth.models import User
from .models  import Diagram
from datetime import datetime
#Create your views here.
def view_diagram(request):
    diagrams = request.user.CreatorOfDiagram.all()
    print(diagrams)
    return render(request,'diagram/view_diagram.html',{ "diagrams":diagrams})


def create_diagram(request):
    if request.method == 'POST':
          title = request.POST.get('title')
          content = request.POST.get('content')
          version = request.POST.get('version')
          diagram = Diagram(title=title,content=content,createdBy=request.user,version=version,lastModified=datetime.now())
          diagram.save()
          return redirect("/authApp/")

    return render(request,'diagram/create_diagram.html')

def edit_diagram(request,diagram_id):
    diagram_obj = Diagram.objects.get(id=diagram_id)
    diagram_obj.version += 1
    if request.method == 'POST':
          diagram_obj.title = request.POST.get('title')
          diagram_obj.label = request.POST.get('label')
          diagram_obj.content = request.POST.get('content')
          diagram_obj.version = request.POST.get('version')
          diagram_obj.save()
          print("diagram changes saved in db")
          return redirect("/authApp/")
    else :
         return render(request,"diagram/edit_diagram.html",{"diagram":diagram_obj})


def delete_diagram(request, diagram_id):
    d = Diagram.objects.get(pk = diagram_id)
    d.delete()
    return redirect('diagram:view_diagram')