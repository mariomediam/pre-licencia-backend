from django.urls import path
from .views import SelectTrabajadorController, LoginController, download_file, downloadFileMedia, BuscarReniecDNIController

urlpatterns= [
    path("buscar-trabajador/", SelectTrabajadorController.as_view()),
    path("login/", LoginController.as_view()),
    path('download/<str:filename>',download_file),
    path('download-file/<str:app>/<str:filename>',downloadFileMedia),
    path("buscar-reniec/", BuscarReniecDNIController.as_view()),
]
