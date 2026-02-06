from django.urls import path

from .views import BuscarRecaudacionSATPController, S42SelectRecaudacionPorAnioyDependenciaController, S42SelectProyeccionPorAnioyDependenciaController, S42SelectRecaudacionPorAnioyTasaController, S42SelectProyeccionPorAnioyTasaController, S42SelectTasaController   

urlpatterns = [
    path('buscar-recaudacion-satp', BuscarRecaudacionSATPController.as_view()),
    path('select-recaudacion-por-anio-y-dependencia', S42SelectRecaudacionPorAnioyDependenciaController.as_view()),
    path('select-proyeccion-por-anio-y-dependencia', S42SelectProyeccionPorAnioyDependenciaController.as_view()),
    path('select-recaudacion-por-anio-y-tasa', S42SelectRecaudacionPorAnioyTasaController.as_view()),
    path('select-proyeccion-por-anio-y-tasa', S42SelectProyeccionPorAnioyTasaController.as_view()),
    path('select-tasa', S42SelectTasaController.as_view()),
]
