from django.urls import path
from .views import (SelectAccesoDepenRequeController
                    ,SelectRequerimientosxDepController
                    ,SelectRequeByIdController
                    ,SelectAniosDepenByIdController)

urlpatterns = [
    path('acceso-depen', SelectAccesoDepenRequeController.as_view()),    
    path('reque-depen', SelectRequerimientosxDepController.as_view()),
    path('reque', SelectRequeByIdController.as_view()),
    path('depen-coddep', SelectAniosDepenByIdController.as_view()),
]