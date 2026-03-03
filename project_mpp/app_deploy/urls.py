from django.urls import path
from .views import (
    SelectTrabajadorController,
    LoginController,
    download_file,
    downloadFileMedia,
    BuscarReniecDNIController,
    BuscarSunatRUCController,
    GenerateQrImageController,
    SelectJefeDepenController,
    ExportJsonToExcelController,
    ExportJsonToExcelMultipleSheetsController,
)

urlpatterns = [
    path("buscar-trabajador/", SelectTrabajadorController.as_view()),
    path("login/", LoginController.as_view()),
    path("download/<str:filename>", download_file),
    path("download-file/<str:app>/<str:filename>", downloadFileMedia),
    path("buscar-reniec/", BuscarReniecDNIController.as_view()),
    path("buscar-sunat/", BuscarSunatRUCController.as_view()),
    path("generate-qr/", GenerateQrImageController.as_view(), name="generate_qr"),
    path("jefe-depen/", SelectJefeDepenController.as_view()),
    # Endpoints genéricos para exportación a Excel
    path("export-json-to-excel/", ExportJsonToExcelController, name="export_json_to_excel"),
    path("export-json-to-excel-multiple/", ExportJsonToExcelMultipleSheetsController, name="export_json_to_excel_multiple"),
]
