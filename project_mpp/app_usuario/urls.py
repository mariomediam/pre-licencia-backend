from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('refresh-session', TokenRefreshView.as_view()),
]