from django.urls import path
from .views import TransporteVigenteView, TranspxAnioView, ComparaTranspxAnioView, TranspxAnioyMesView, InfraccionesTransportexAnioView, ComparaInfraccTransportexAnioView, TranspAntigVehicView

urlpatterns = [
    path("vehiculos-vigentes/", TransporteVigenteView.as_view()),
    path("vehiculos-autorizados/", TranspxAnioView.as_view()),
    path("comparacion-vehiculos-autorizados/", ComparaTranspxAnioView.as_view()),
    path("vehiculos-autorizados-mes/", TranspxAnioyMesView.as_view()),
    path("infracciones-transporte/", InfraccionesTransportexAnioView.as_view()),
    path("comparacion-infracciones-transporte/", ComparaInfraccTransportexAnioView.as_view()),
    path("antiguedad-vehiculos/", TranspAntigVehicView.as_view()),
]
