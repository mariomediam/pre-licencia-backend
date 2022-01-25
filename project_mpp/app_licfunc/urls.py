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
                PrecalTipoDocumController,)

urlpatterns = [
    path('precalificacion', PrecalificacionController.as_view()),    
    path('eval-usu/<str:login>', EvalUsuController.as_view()),
    path('precal-usu-estado', PrecalifUserEstadoController.as_view()),
    path('precalificacion/<int:id>', PrecalifContribController.as_view()),    
    path('precal-giro-neg/<int:precalId>', PrecalifGiroNegController.as_view()),    
    path('precal-cuestionario/<int:precalId>', PrecalifCuestionarioController.as_view()),
    path('precal-eval/<int:precalId>', PrecalEvaluacionController.as_view()),
    path('precal-eval/<int:precalId>/<int:tipoEvalId>', PrecalEvaluacionTipoController.as_view()),
    path('precal-eval-docum/<int:precalId>/<int:tipoEvalId>', PrecalDocumentacionController.as_view()),
    path('tipo-eval', TipoEvalController.as_view()),
    path('tipo-docum', PrecalTipoDocumController.as_view()),
]