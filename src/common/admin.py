from django.contrib import admin

from .models import Client, Expert, Project, CommentForExpert, CommentForClient, Image
# Register your models here.
admin.site.register(Client)
admin.site.register(Expert)
admin.site.register(Project)
admin.site.register(CommentForExpert)
admin.site.register(CommentForClient)
admin.site.register(Image)