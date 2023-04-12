from django.urls import path
from .views import GenerateBoletasPdfController

urlpatterns= [
    path("genera-boletas/", GenerateBoletasPdfController.as_view()),
]
