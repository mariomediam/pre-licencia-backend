from django.urls import path
from .views import (SelectAccesoDepenRequeController
                    ,SelectRequerimientosxDepController
                    ,SelectRequeByIdController
                    ,SelectAniosDepenByIdController
                    ,SelectSaldoPresupDepenController)

urlpatterns = [
    path('acceso-depen', SelectAccesoDepenRequeController.as_view()),    
    path('reque-depen', SelectRequerimientosxDepController.as_view()),
    path('reque', SelectRequeByIdController.as_view()),
    path('depen-coddep', SelectAniosDepenByIdController.as_view()),
    path('saldo-depen', SelectSaldoPresupDepenController.as_view()),
]