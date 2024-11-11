from django.urls import path
from .views import MaestroDocumentoView, PersonaView, ProveedorSIGAView

urlpatterns = [
    path("maestro-documento/", MaestroDocumentoView.as_view()),
    path("persona/", PersonaView.as_view()),
    path("proveedor-siga/", ProveedorSIGAView.as_view()),
]