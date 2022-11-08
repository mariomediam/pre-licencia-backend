from django.urls import path
from .views import (PrecalificacionController, 
                EvalUsuController,
                PrecalifUserEstadoController,
                PrecalifContribController,
                PrecalifGiroNegController,
                PrecalifCuestionarioController,
                PrecalEvaluacionController,
                PrecalEvaluacionTipoController,
                PrecalDocumentacionController,
                TipoEvalController,
                PrecalTipoDocumController,
                SubirImagenController,
                TipoLicenciaController,
                SectoresLicController,
                SectoresBuscarController,
                SectoresPorPrecalificacionController,
                TipoLicenciaPorIdController,
                BuscarRequisitoArchivoController,
                prelicenciaDownloadFile,
                prelicenciaPreviewFile,
                agregarPreLicenciaFirma,
                prelicenciaPreviewFirmaFile,
                EliminarPreLicenciaFirma,
                VistoBuenoDcPreLicencia,
                VistoBuenoDlPreLicencia,
                PrecalifUserEstadoPaginationController,
                EnviarCorreoTerminalistaController,
                GiroNegocioPaginationController,
                PrecalificacionPruebaController,
                LicencArchivoController,
                AgregarLicencArchivoController,
                licenciaPreviewFile,
                licenciaDownloadFile,
                )

urlpatterns = [
    path('precalificacion', PrecalificacionController.as_view()),    
    path('eval-usu/<str:login>', EvalUsuController.as_view()),
    path('precal-usu-estado', PrecalifUserEstadoController.as_view()),
    path('precalificacion/<int:id>', PrecalifContribController.as_view()),    
    path('precal-giro-neg/<int:precalId>', PrecalifGiroNegController.as_view()),    
    path('precal-cuestionario/<int:precalId>', PrecalifCuestionarioController.as_view()),
    path('precal-eval/<int:precalId>', PrecalEvaluacionController.as_view()),
    path('precal-eval/<int:precalId>/<int:tipoEvalId>', PrecalEvaluacionTipoController.as_view()),
    path('precal-eval/subir-imagen', SubirImagenController.as_view()),
    path('precal-eval-docum/<int:precalId>/<int:tipoEvalId>', PrecalDocumentacionController.as_view()),
    path('tipo-eval', TipoEvalController.as_view()),
    path('tipo-docum', PrecalTipoDocumController.as_view()),
    path('tipo-licencia', TipoLicenciaController.as_view()),
    path('tipo-licencia/<str:tipoLicenciaId>', TipoLicenciaPorIdController.as_view()),    
    path('sectores', SectoresLicController.as_view()),
    path('sector-buscar', SectoresBuscarController.as_view()),
    path('sector-precal', SectoresPorPrecalificacionController.as_view()),
    path('requisito-archivo', BuscarRequisitoArchivoController.as_view()),
    path('download/requisito-archivo/<int:id>',prelicenciaDownloadFile),
    path('view/requisito-archivo/<int:id>',prelicenciaPreviewFile),    
    path('agregar-firma-archivo/<int:id>',agregarPreLicenciaFirma.as_view()),
    path('eliminar-firma-archivo/<int:id>',EliminarPreLicenciaFirma.as_view()),
    path('view/firma-archivo/<int:id>',prelicenciaPreviewFirmaFile),    
    path('precal-vb-dc/<int:id>',VistoBuenoDcPreLicencia.as_view()),
    path('precal-vb-dl/<int:id>',VistoBuenoDlPreLicencia.as_view()),
    path('precal-usu-estado-p', PrecalifUserEstadoPaginationController.as_view()),
    path('precal-alerta/<int:precalId>', EnviarCorreoTerminalistaController.as_view()),
    path('giro-negocio-p', GiroNegocioPaginationController.as_view()),
    path('licenc-archivo/<int:licenc_file>', LicencArchivoController.as_view()),
    path('licenc-archivo', AgregarLicencArchivoController.as_view()),
    path('prueba', PrecalificacionPruebaController.as_view()),
    path('view/licencia/<int:id>',licenciaPreviewFile),    
    path('download/licencia/<int:id>',licenciaDownloadFile),
]