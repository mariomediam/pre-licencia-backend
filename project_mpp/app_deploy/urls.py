from django.urls import path
from .views import SelectTrabajadorController, LoginController

urlpatterns= [
    path("buscar-trabajador/", SelectTrabajadorController.as_view()),
    path("login/", LoginController.as_view())
]
