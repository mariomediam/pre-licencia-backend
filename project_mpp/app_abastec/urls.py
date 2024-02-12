from django.urls import path
from .views import (SelectAccesoDepenRequeController
                    ,SelectRequerimientosxDepController)

urlpatterns = [
    path('acceso-depen', SelectAccesoDepenRequeController.as_view()),    
    path('reque-depen', SelectRequerimientosxDepController.as_view()),
]