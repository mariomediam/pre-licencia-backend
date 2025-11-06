from django.urls import path
from .views import (ExpedientesController, SeleccDocumController)

urlpatterns = [
    path('expedientes/<str:numero>/<str:anio>', ExpedientesController.as_view()),
    path('selecc-docum', SeleccDocumController.as_view()),
]