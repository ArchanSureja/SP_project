from django.db import models
from django.contrib.auth.models import User 
# Create your models here.

class Template(models.Model):
    title = models.CharField(max_length=64)
    content = models.TextField()
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE,related_name="CreatorOfTemplate")

class Note(models.Model):
    title = models.CharField(max_length=64)
    createdBy = models.ForeignKey(User,on_delete=models.CASCADE,related_name="creator")
    label = models.CharField(max_length=64)
    version = models.IntegerField()
    lastModified = models.DateTimeField()
    modifications = models.TextField(default=None)
    templateUsed = models.ForeignKey(Template,default=None,on_delete=models.CASCADE,related_name="TemplateUsedis", null=True)

class Media(models.Model):
    media_type = models.CharField(max_length=64)
    details = models.CharField(max_length=64)
    belong_to = models.ForeignKey(Note,on_delete=models.CASCADE,default=None)


class Text(models.Model):
    data = models.TextField()
    style = models.CharField(max_length=64)
    IsBold = models.BooleanField(default=False)
    IsItalic = models.BooleanField(default=False)
    IsUnderline = models.BooleanField(default=False)
    align = models.CharField(max_length=64)
    belong_to = models.ForeignKey(Note,default=None,on_delete=models.CASCADE)

    
class collabs(models.Model):
    note_id=models.ForeignKey(Note,on_delete=models.CASCADE)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    permission=models.CharField(max_length=50)