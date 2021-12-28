from django.contrib.auth.backends import BaseBackend
from app_usuario.models import UsuarioModel
from .usuario import login

class MyBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if username is None:
            return None

        miUsuario = None

        resultado = login(username, password)

        if resultado[0]['estado'].strip() == "OK":
            miUsuario = UsuarioModel.objects.get(pk=username)

        return miUsuario

    def get_user(self, username):
        try:
            return UsuarioModel.objects.get(pk=username)
        except Exception:
            print("Error")
            return None

