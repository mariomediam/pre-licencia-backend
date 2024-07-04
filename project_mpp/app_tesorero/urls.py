from django.urls import path
from .views import UploadFileTributo, TributoTipoOperacionView, TributoArchivoView



urlpatterns= [
    # path("genera-boletas/", GenerateBoletasPdfController.as_view()),
    path("upload-file-tributo/", UploadFileTributo.as_view()),
    path("tributo-tipo-operacion/", TributoTipoOperacionView.as_view()),
    path("tributo-archivo/", TributoArchivoView.as_view())
   
]
