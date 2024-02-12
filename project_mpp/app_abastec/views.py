from rest_framework.generics import (
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from app_abastec.abastec import (SelectAccesoDepenReque,
                                 SelectRequeSf_dep)

# Create your views here.
class SelectAccesoDepenRequeController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        anio = request.query_params.get("anio")
        login = request.user.username
        depen = request.query_params.get("depen", None)
        filtro = request.query_params.get("filtro", None)

        if anio:            
            requisito_archivo = SelectAccesoDepenReque(anio, login, depen, filtro)
            return Response(data={"message": None, "content": requisito_archivo}, status=200)

        else:
            return Response(
                data={"message": "Debe de ingresar año buscado"},
                status=status.HTTP_404_NOT_FOUND,
            )


# Create your views here.
class SelectRequerimientosxDepController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:
            
            anio = request.query_params.get("anio")        
            sf_dep = request.query_params.get("sfdep")
            bie_ser_tipo = request.query_params.get("tipo")
            field = request.query_params.get("field", None)
            valor = request.query_params.get("valor", None)
            libre = request.query_params.get("libre", None)
            tipo_gasto = request.query_params.get("tipogasto", None)
            
            if anio and sf_dep and bie_ser_tipo:            
                requerimientos = SelectRequeSf_dep(anio, sf_dep, bie_ser_tipo, field, valor, libre, tipo_gasto)
                return Response(data={"message": None, "content": requerimientos}, status=200)

            else:
                return Response(
                    data={"message": "Debe de ingresar año, dependencia y tipo de requerimiento buscado","content": None},
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e),"content": None},
                status=status.HTTP_404_NOT_FOUND,
            )

