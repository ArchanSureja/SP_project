from django.contrib import admin
from .models import Media,Text,Note,Template,collabs
# Register your models here.
admin.site.register(Media)
admin.site.register(Text)
admin.site.register(Note)
admin.site.register(Template)
admin.site.register(collabs)