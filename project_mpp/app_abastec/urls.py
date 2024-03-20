from django.urls import path
from .views import (SelectAccesoDepenRequeController
                    ,SelectRequerimientosxDepController
                    ,SelectRequeByIdController
                    ,SelectAniosDepenByIdController
                    ,SelectSaldoPresupDepenController
                    ,SelectBBSSDisponibleOrdenController
                    ,RequerimientoController
                    ,SelectSaldoPresupRequeController
                    ,SelectRequeFuentesController
                    ,SelectSaldoPresupRequeItemController
                    ,RequePrecomprometerController)

urlpatterns = [
    path('acceso-depen', SelectAccesoDepenRequeController.as_view()),    
    path('reque-depen', SelectRequerimientosxDepController.as_view()),
    path('reque', SelectRequeByIdController.as_view()),
    path('reque/<str:anio>/<str:numero>/<str:tipo>', RequerimientoController.as_view()),
    path('depen-coddep', SelectAniosDepenByIdController.as_view()),
    path('saldo-depen', SelectSaldoPresupDepenController.as_view()),
    path('bbss-disponible-orden', SelectBBSSDisponibleOrdenController.as_view()),
    path('reque-saldo-presup', SelectSaldoPresupRequeController.as_view()),
    path('reque-fuentes', SelectRequeFuentesController.as_view()),
    path('reque-saldo-presup-item', SelectSaldoPresupRequeItemController.as_view()),
    path('reque-precompromete/<str:anio>/<str:numero>/<str:tipo>', RequePrecomprometerController.as_view()),
]
