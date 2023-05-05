from django.urls import path
from .views import GenerateBoletasPdfController, SelectPlanillaBoletaController, ListaPlanillaResumenController, SelectPlanillaBoletaGeneradoController

urlpatterns= [
    path("genera-boletas/", GenerateBoletasPdfController.as_view()),
    path("lista-planilla-boleta/", SelectPlanillaBoletaController.as_view()),
    path("lista-planilla-detalle/", ListaPlanillaResumenController.as_view()),
    path("lista-planilla-generado/", SelectPlanillaBoletaGeneradoController.as_view()),
]
