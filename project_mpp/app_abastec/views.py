from operator import itemgetter

from rest_framework.generics import (
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from app_abastec.abastec import (
    SelectAccesoDepenReque,
    SelectRequeSf_dep,
    SelectRequeById,
    SelectAniosDepenById,
    SelectSaldoPresupDepen,
)


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
            return Response(
                data={"message": None, "content": requisito_archivo}, status=200
            )

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
                requerimientos = SelectRequeSf_dep(
                    anio, sf_dep, bie_ser_tipo, field, valor, libre, tipo_gasto
                )
                return Response(
                    data={"message": None, "content": requerimientos}, status=200
                )

            else:
                return Response(
                    data={
                        "message": "Debe de ingresar año, dependencia y tipo de requerimiento buscado",
                        "content": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )


class SelectRequeByIdController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:

            anio = request.query_params.get("anio")
            numero = request.query_params.get("numero")
            bie_ser_tipo = request.query_params.get("tipo")

            if anio and numero and bie_ser_tipo:
                requerimiento = SelectRequeById(anio, numero, bie_ser_tipo)

                if len(requerimiento) == 0:
                    requerimiento_return = {}
                else:
                    requerimiento_return = requerimiento[0]

                return Response(
                    data={"message": None, "content": requerimiento_return}, status=200
                )

            else:
                return Response(
                    data={
                        "message": "Debe de ingresar año, numero y tipo de requerimiento buscado",
                        "content": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )


class SelectAniosDepenByIdController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:
            anio = request.query_params.get("anio")
            cod_dep = request.query_params.get("coddep")

            if anio and cod_dep:
                dependencia = SelectAniosDepenById(anio, cod_dep)

                if len(dependencia) == 0:
                    dependencia_return = {}
                else:
                    dependencia_return = dependencia[0]

                return Response(
                    data={"message": None, "content": dependencia_return}, status=200
                )

            else:
                return Response(
                    data={
                        "message": "Debe de ingresar año y código de dependencia buscado",
                        "content": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )


class SelectSaldoPresupDepenController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:
            anio = request.query_params.get("anio")
            cod_dep = request.query_params.get("coddep")
            bie_ser_tipo = request.query_params.get("tipo")
            formato = request.query_params.get("formato")

            if anio and cod_dep:
                saldo = SelectSaldoPresupDepen(anio, cod_dep, bie_ser_tipo)

                if formato == "reque":
                    keys = ['C_anipre', 'C_secfun', 'N_metapresup_desc', 'C_depen', 'C_activpoi', 'N_activpoi_desc', 'C_clapre', 'C_objpoi', 'C_metapoi']
                    saldo.sort(key=itemgetter(*keys))

                    saldo_format = []

                    i = 0
                    secfun = ""
                    depen = ""
                    activ_poi = ""
                    clapre = ""
                    objpoi = ""
                    metapoi = ""
                    row = {}

                    while i < len(saldo):
                        if secfun != saldo[i]["C_secfun"]:
                            if i != 0:
                                saldo_format.append(row)

                            row = {"C_anipre": saldo[i]["C_anipre"], "C_secfun": saldo[i]["C_secfun"], "N_metapresup_desc": saldo[i]["N_metapresup_desc"], "actividades": []}

                        if activ_poi != saldo[i]["C_activpoi"] or depen != saldo[i]["C_depen"]:                            
                            actividad = {"C_activpoi": saldo[i]["C_activpoi"], "N_activpoi_desc": saldo[i]["N_activpoi_desc"], "clasificadores": []}
                            row["actividades"].append(actividad)

                        if clapre != saldo[i]["C_clapre"] or objpoi != saldo[i]["C_objpoi"] or metapoi != saldo[i]["C_metapoi"]:
                            clasificador = {"C_clapre": saldo[i]["C_clapre"], "C_objpoi": saldo[i]["C_objpoi"], "C_metapoi": saldo[i]["C_metapoi"], "saldos": []}
                            row["actividades"][-1]["clasificadores"].append(clasificador)

                        row["actividades"][-1]["clasificadores"][-1]["saldos"].append({"C_fuefin": saldo[i]["C_fuefin"], "C_recurso": saldo[i]["C_recurso"], "Q_monto": saldo[i]["Q_monto"]})                                                                            

                        secfun = saldo[i]["C_secfun"]
                        depen = saldo[i]["C_depen"]
                        activ_poi = saldo[i]["C_activpoi"]
                        clapre = saldo[i]["C_clapre"]
                        objpoi = saldo[i]["C_objpoi"]
                        metapoi = saldo[i]["C_metapoi"]

                        i += 1
                    
                    saldo_format.append(row)

                    saldo = saldo_format

                return Response(data={"message": None, "content": saldo}, status=200)

            else:
                return Response(
                    data={
                        "message": "Debe de ingresar año, código de dependencia y tipo de bien o servicio buscado",
                        "content": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )
