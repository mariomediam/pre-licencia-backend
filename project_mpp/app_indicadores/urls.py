from django.urls import path

from .views import BuscarRecaudacionSATPController

urlpatterns = [
    path('buscar-recaudacion-satp', BuscarRecaudacionSATPController.as_view()),
]
