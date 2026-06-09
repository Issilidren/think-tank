from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('voting.urls')),
    path('', lambda req: redirect('voting:project', project_id=1)),
]
