from django.urls import path
from .views import MaestroDocumentoView, PersonaView, ProveedorSIGAView, SeleccionarExpedienteFase, SeleccionarExpedienteSecuencia, DownloadFormatoDevengadoController, ProcesoActualizarRegistroView, BuscarCartaOrdenView, DownloadCartaOrdenFideicomisoController, SincroGastoDiario, UltimaSincronizacionView, ProgProyectosInversionMensualView, ProductoProyectoNombreView, UltimaSincronizacionAnioView, ResumenProductoProyectoView, ProyectoInversionView, ProgramacionProyectoInversionView, DownloadProyeccionMensualView, ObtenerMontosPorAnioView, ContarProyectosPorAnioView, EjecucionMesView, EjecucionEsperadaView, ResumenProyectosView

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
    path("sincro-gasto-diario", SincroGastoDiario.as_view()),
    path("ultima-sincro", UltimaSincronizacionView.as_view()),
    path("proyectos-programacion-mensual", ProgProyectosInversionMensualView.as_view()),
    path("producto-proyecto-nombre", ProductoProyectoNombreView.as_view()),
    path("ultima-sincro-anio", UltimaSincronizacionAnioView.as_view()),
    path("resumen-producto-proyecto", ResumenProductoProyectoView.as_view()),
    path("proyecto-inversion", ProyectoInversionView.as_view()),
    path("programacion-proyecto-inversion", ProgramacionProyectoInversionView.as_view()),
    path("programacion-proyecto-inversion/<int:c_prgpro>", ProgramacionProyectoInversionView.as_view()),
    path("download-proyeccion-mensual", DownloadProyeccionMensualView),
    path("obtener-montos-por-anio", ObtenerMontosPorAnioView.as_view()),
    path("contar-proyectos-por-anio", ContarProyectosPorAnioView.as_view()),
    path("ejecucion-mes", EjecucionMesView.as_view()),
    path("ejecucion-esperada", EjecucionEsperadaView.as_view()),
    path("resumen-proyectos", ResumenProyectosView.as_view()),
]
