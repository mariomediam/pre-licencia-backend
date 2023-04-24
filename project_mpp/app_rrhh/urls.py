from django.urls import path
from .views import GenerateBoletasPdfController, SelectPlanillaBoletaController, ListaPlanillaResumenController

urlpatterns= [
    path("genera-boletas/", GenerateBoletasPdfController.as_view()),
    path("lista-planilla-boleta/", SelectPlanillaBoletaController.as_view()),
    path("lista-planilla-detalle/", ListaPlanillaResumenController.as_view()),
]
