from django.urls import path
from .views import MaestroDocumentoView, PersonaView, ProveedorSIGAView, SeleccionarExpedienteFase, SeleccionarExpedienteSecuencia, DownloadFormatoDevengadoController, ProcesoActualizarRegistroView, BuscarCartaOrdenView, DownloadCartaOrdenFideicomisoController

urlpatterns = [
    path("maestro-documento/", MaestroDocumentoView.as_view()),
    path("persona/", PersonaView.as_view()),
    path("proveedor-siga/", ProveedorSIGAView.as_view()),
    path("seleccionar-expediente-fase", SeleccionarExpedienteFase.as_view()),
    path("seleccionar-expediente-secuencia", SeleccionarExpedienteSecuencia.as_view()),
    path("download-formato-devengado", DownloadFormatoDevengadoController),
    path("proceso-actualizar-registro", ProcesoActualizarRegistroView.as_view()),
    path("buscar-carta-orden", BuscarCartaOrdenView.as_view()),
    path("download-carta-orden-fideicomiso", DownloadCartaOrdenFideicomisoController),
]
