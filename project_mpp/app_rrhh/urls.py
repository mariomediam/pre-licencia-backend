from django.urls import path
from .views import GenerateBoletasPdfController, SelectPlanillaBoletaController

urlpatterns= [
    path("genera-boletas/", GenerateBoletasPdfController.as_view()),
    path("lista-planilla-boleta/", SelectPlanillaBoletaController.as_view()),
]
