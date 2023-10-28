from django.urls import path
from .views import (ExpedientesController,)

urlpatterns = [
    path('expedientes/<str:numero>/<str:anio>', ExpedientesController.as_view()),
]