from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='ocrfiles'),
    path('<int:ocr_id>/<int:page_number>', views.validation, name='validation'),
    path('search', views.search, name='search'),
]
