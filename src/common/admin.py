from django.contrib import admin

from .models import Client, Expert, Project
# Register your models here.
admin.site.register(Client)
admin.site.register(Expert)
admin.site.register(Project)