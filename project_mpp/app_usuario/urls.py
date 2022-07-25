from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from .views import MenuesController, UserMenuesController                                          

urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('refresh-session', TokenRefreshView.as_view()),
    path('menues', MenuesController.as_view()), 
    path('usermenues', UserMenuesController.as_view()), 
]