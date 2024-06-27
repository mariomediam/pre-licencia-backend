from django.urls import path
from .views import *



urlpatterns= [
    # path("genera-boletas/", GenerateBoletasPdfController.as_view()),
    path("upload-file-tributo/", UploadFileTributo.as_view()),
   
]
