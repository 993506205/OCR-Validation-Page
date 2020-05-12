from django.urls import path, include

from . import views

urlpatterns = [
    path('createProject/', views.prj_create, name='createnew'),
]