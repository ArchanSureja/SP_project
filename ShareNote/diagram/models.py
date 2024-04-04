from django.db import models
from django.contrib.auth.models import User 

# Create your models here.


class Diagram(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE,related_name="CreatorOfDiagram")
    version = models.IntegerField()
    lastModified = models.DateTimeField()

    # we store shape as json format then at rendering time we use draw.io js library to render the diagram from json format 