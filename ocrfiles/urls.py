from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='ocrfiles'),
    path('addNew/<int:dirprj_id>', views.addNew, name='addNew'),
    path('<int:ocr_id>/<int:page_number>', views.validation, name='validation'),
    path('search', views.search, name='search'),
]
