from django.urls import path

from .views import (BuscarContribNombreController,
    BuscarContribCodigoController,
    ConsultaContribCodigoController,
    ConsultaDocumentoNumeroController,
    ListarTipoContribuyenteController,
    ConsultaTipoLugarController,
    ConsultaSectoresController,
    ConsultaLugarGeneralController,
    ConsultaTipLugController,
    BuscarContribPaginationController)

urlpatterns = [
    path('buscar-contribuyente-nombre', BuscarContribNombreController.as_view()),
    path('buscar-contribuyente-codigo', BuscarContribCodigoController.as_view()),
    path('consultar-contribuyente-codigo', ConsultaContribCodigoController.as_view()),
    path('consultar-documento-numero', ConsultaDocumentoNumeroController.as_view()),
    path('tipo-contribuyente', ListarTipoContribuyenteController.as_view()),
    path('tipo-lugar', ConsultaTipoLugarController.as_view()),
    path('sector', ConsultaSectoresController.as_view()),
    path('consultar-lugar-general', ConsultaLugarGeneralController.as_view()),
    path('consultar-tiplug-codigo', ConsultaTipLugController.as_view()),
    path('buscar-contribuyente-p', BuscarContribPaginationController.as_view()),
]