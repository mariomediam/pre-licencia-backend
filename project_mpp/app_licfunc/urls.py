from django.urls import path
from .views import (PrecalificacionController, 
                EvalUsuController,
                PrecalifUserEstadoController,
                PrecalifContribController,
                PrecalifGiroNegController,
                PrecalifCuestionarioController)

urlpatterns = [
    path('precalificacion', PrecalificacionController.as_view()),    
    path('eval-usu/<str:login>', EvalUsuController.as_view()),
    path('precal-usu-estado', PrecalifUserEstadoController.as_view()),
    path('precalificacion/<int:id>', PrecalifContribController.as_view()),    
    path('precal-giro-neg/<int:precalId>', PrecalifGiroNegController.as_view()),    
    path('precal-cuestionario/<int:precalId>', PrecalifCuestionarioController.as_view()),    
]