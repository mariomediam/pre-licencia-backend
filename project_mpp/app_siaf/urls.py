from django.urls import path
from .views import MaestroDocumentoView, PersonaView, ProveedorSIGAView, SeleccionarExpedienteFase, SeleccionarExpedienteSecuencia, DownloadFormatoDevengadoController

urlpatterns = [
    path("maestro-documento/", MaestroDocumentoView.as_view()),
    path("persona/", PersonaView.as_view()),
    path("proveedor-siga/", ProveedorSIGAView.as_view()),
    path("seleccionar-expediente-fase", SeleccionarExpedienteFase.as_view()),
    path("seleccionar-expediente-secuencia", SeleccionarExpedienteSecuencia.as_view()),
    path("download-formato-devengado", DownloadFormatoDevengadoController),
]
