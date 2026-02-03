from django.urls import path

from .views import BuscarRecaudacionSATPController, S42SelectRecaudacionPorAnioyDependenciaController, S42SelectProyeccionPorAnioyDependenciaController   

urlpatterns = [
    path('buscar-recaudacion-satp', BuscarRecaudacionSATPController.as_view()),
    path('select-recaudacion-por-anio-y-dependencia', S42SelectRecaudacionPorAnioyDependenciaController.as_view()),
    path('select-proyeccion-por-anio-y-dependencia', S42SelectProyeccionPorAnioyDependenciaController.as_view()),
]
