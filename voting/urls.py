from django.urls import path
from . import views

app_name = 'voting'

urlpatterns = [
    path('project/<int:project_id>/', views.project_view, name='project'),
]
