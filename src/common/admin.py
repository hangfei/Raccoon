from django.contrib import admin

from .models import Client, Expert, Project, CommentForExpert
# Register your models here.
admin.site.register(Client)
admin.site.register(Expert)
admin.site.register(Project)
admin.site.register(CommentForExpert)