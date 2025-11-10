from django.urls import path
from .views import (ExpedientesController, SeleccDocumController, VerArbolController, VerUltimaRamaArbolController)

urlpatterns = [
    path('expedientes/<str:numero>/<str:anio>', ExpedientesController.as_view()),
    path('selecc-docum', SeleccDocumController.as_view()),
    path('ver-arbol', VerArbolController.as_view()),
    path('ver-ultima-rama-arbol', VerUltimaRamaArbolController.as_view()),
]