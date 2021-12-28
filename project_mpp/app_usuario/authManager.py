from django.contrib.auth.models import BaseUserManager


class ManejoUsuarios(BaseUserManager):
    def test_user(self, username):        
        return username

    def is_password_usable(self, encoded_password):
        return True