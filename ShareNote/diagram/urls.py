from django.urls import path
from . import views 
app_name="diagram"
urlpatterns = [
    path("",views.view_diagram,name="view_diagram"),
    path("create",views.create_diagram,name="create_diagram"),
    path("<int:diagram_id>",views.edit_diagram,name="edit_diagram"),
    path("delete/<int:diagram_id>",views.delete_diagram,name="delete_diagram")
  
]