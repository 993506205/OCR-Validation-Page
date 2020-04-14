from django.urls import path

from . import views

urlpatterns = [
    path('', views.prj_create, name='createnew'),
]