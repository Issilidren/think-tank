from django.contrib import admin
from .models import Handle, Project, Idea, Theme, Vote

admin.site.register(Handle)
admin.site.register(Project)
admin.site.register(Idea)
admin.site.register(Theme)
admin.site.register(Vote)
