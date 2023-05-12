from django.urls import path
from .views import GenerateBoletasPdfController, SelectPlanillaBoletaController, ListaPlanillaResumenController, SelectPlanillaBoletaGeneradoController, SelectPlanillaTrabajadorCorreoController, SelectTipoPlanillaxTipoController, SendEmailBoletaController, SelectBoletaEnvioController, SelectTrabajadorCorreoPaginationController, SelectTrabajadorCorreoController

urlpatterns= [
    path("genera-boletas/", GenerateBoletasPdfController.as_view()),
    path("lista-planilla-boleta/", SelectPlanillaBoletaController.as_view()),
    path("lista-planilla-detalle/", ListaPlanillaResumenController.as_view()),
    path("lista-planilla-generado/", SelectPlanillaBoletaGeneradoController.as_view()),
    path("lista-planilla-correo/", SelectPlanillaTrabajadorCorreoController.as_view()),
    path("tipo-planilla-xtipo/", SelectTipoPlanillaxTipoController.as_view()),
    path("enviar-boletas/", SendEmailBoletaController.as_view()),
    path("lista-boleta-envio/", SelectBoletaEnvioController.as_view()),
    path("lista-trabajador-correo-p/", SelectTrabajadorCorreoPaginationController.as_view()),
    path("lista-trabajador-correo/", SelectTrabajadorCorreoController.as_view()),
]
