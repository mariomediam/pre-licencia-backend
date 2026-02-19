from django.urls import path
from .views import TransporteVigenteView, TranspxAnioView, ComparaTranspxAnioView, TranspxAnioyMesView, InfraccionesTransportexAnioView, ComparaInfraccTransportexAnioView, TranspAntigVehicView, OcurrenciasxAnioView, MontosPapeletaTransitoView, ComparaMontosPapeletaTransitoView, S42CapacitacionController, S42SelectCapacitacionObservacionController

urlpatterns = [
    path("vehiculos-vigentes/", TransporteVigenteView.as_view()),
    path("vehiculos-autorizados/", TranspxAnioView.as_view()),
    path("comparacion-vehiculos-autorizados/", ComparaTranspxAnioView.as_view()),
    path("vehiculos-autorizados-mes/", TranspxAnioyMesView.as_view()),
    path("infracciones-transporte/", InfraccionesTransportexAnioView.as_view()),
    path("comparacion-infracciones-transporte/", ComparaInfraccTransportexAnioView.as_view()),
    path("antiguedad-vehiculos/", TranspAntigVehicView.as_view()),
    path("ocurrencias-anio/", OcurrenciasxAnioView.as_view()),
    path("montos-papeleta/", MontosPapeletaTransitoView.as_view()),
    path("comparacion-montos-papeleta/", ComparaMontosPapeletaTransitoView.as_view()),
    path("capacitacion/", S42CapacitacionController.as_view()),
    path("capacitacion-observacion/", S42SelectCapacitacionObservacionController.as_view()),
]
