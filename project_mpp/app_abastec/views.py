import sys
import traceback
import os
from datetime import datetime

from operator import itemgetter

from rest_framework.generics import (
    RetrieveAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes

from django.template.loader import get_template, render_to_string
from django.template import Context
from django.http import HttpResponse
from django.conf import settings

import pdfkit
import uuid

from app_abastec.abastec import (
    SelectAccesoDepenReque,
    SelectRequeSf_dep,
    SelectRequeById,
    SelectAniosDepenById,
    SelectSaldoPresupDepen,
    SelectBBSSDisponibleOrden,
    InsertRequeMyXML,
    SelectRequeDetalle,
    DeleteRequeDetalle,
    SelectSaldoPresupReque,
    RequeFuentes,
    SelectSaldoPresupRequeItem,
    PrecompromisoReque,
    AnularDocumentos,
    SelectExpedienteFase,
    SelectTipo_Certificacion,
    ListaRequeGasto,
    ListaReque,
    SelectReque,
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
                    keys = [
                        "C_anipre",
                        "C_secfun",
                        "N_metapresup_desc",
                        "C_depen",
                        "C_activpoi",
                        "N_activpoi_desc",
                        "C_clapre",
                        "C_objpoi",
                        "C_metapoi",
                    ]
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
                                secfun = ""
                                depen = ""
                                activ_poi = ""
                                clapre = ""
                                objpoi = ""
                                metapoi = ""

                            row = {
                                "C_anipre": saldo[i]["C_anipre"],
                                "C_secfun": saldo[i]["C_secfun"],
                                "N_metapresup_desc": saldo[i]["N_metapresup_desc"],
                                "actividades": [],
                            }

                        if (
                            activ_poi != saldo[i]["C_activpoi"]
                            or depen != saldo[i]["C_depen"]
                        ):
                            actividad = {
                                "C_activpoi": saldo[i]["C_activpoi"],
                                "N_activpoi_desc": saldo[i]["N_activpoi_desc"],
                                "C_depen": saldo[i]["C_depen"],
                                "clasificadores": [],
                            }
                            row["actividades"].append(actividad)

                        if (
                            clapre != saldo[i]["C_clapre"]
                            or objpoi != saldo[i]["C_objpoi"]
                            or metapoi != saldo[i]["C_metapoi"]
                        ):
                            clasificador = {
                                "C_clapre": saldo[i]["C_clapre"],
                                "C_objpoi": saldo[i]["C_objpoi"],
                                "C_metapoi": saldo[i]["C_metapoi"],
                                "saldos": [],
                                "selecc": False,
                            }
                            row["actividades"][-1]["clasificadores"].append(
                                clasificador
                            )

                        row["actividades"][-1]["clasificadores"][-1]["saldos"].append(
                            {
                                "C_fuefin": saldo[i]["C_fuefin"],
                                "C_recurso": saldo[i]["C_recurso"],
                                "Q_monto": saldo[i]["Q_monto"],
                            }
                        )

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
            # exc_type, exc_value, exc_traceback = sys.exc_info()
            # line_number = traceback.tb_lineno(exc_traceback.tb_next)
            # print(f"An error occurred at line {line_number}: {e}")
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )


class SelectBBSSDisponibleOrdenController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:
            anio = request.query_params.get("anio")
            sec_fun = request.query_params.get("secfun", "")
            cod_dep = request.query_params.get("coddep", "")
            bie_ser_tipo = request.query_params.get("tipo")
            file = request.query_params.get("file")
            valor = request.query_params.get("valor")

            if anio and bie_ser_tipo and file and valor:
                bienes_servicios = SelectBBSSDisponibleOrden(
                    anio, sec_fun, cod_dep, bie_ser_tipo, file, valor
                )

                return Response(
                    data={"message": None, "content": bienes_servicios}, status=200
                )

            else:
                return Response(
                    data={
                        "message": "Debe de ingresar año, tipo de bien o servicio y valor buscado",
                        "content": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )


class RequerimientoController(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, anio, numero, tipo):

        try:

            if anio and numero and tipo:
                requerimiento = SelectRequeById(anio, numero, tipo)

                if len(requerimiento) == 0:
                    requerimiento_return = {}
                else:
                    requerimiento_return = requerimiento[0]
                    detalle = SelectRequeDetalle(anio, numero, tipo)

                    key_mapping = {
                        "c_clapre": "C_clapre",
                        "C_ITEM": "C_item",
                        "N_BIESER_DESC": "N_bieser_desc",
                        "N_UNIMED_DESC": "N_unimed_desc",
                    }
                    datalle_format = []

                    for item in detalle:
                        updated_json = {
                            key_mapping.get(key, key): value
                            for key, value in item.items()
                        }
                        datalle_format.append(updated_json)

                    keys = [
                        "C_clapre",
                        "C_secfun",
                        "C_depen",
                        "C_activpoi",
                        "C_objpoi",
                        "C_metapoi",
                    ]
                    clasificadores_dict = {}

                    for item in datalle_format:
                        # Creamos una tupla con los valores de las claves que nos interesan
                        tuple_keys = tuple(item[key] for key in keys)

                        # Si la tupla no está en el diccionario, la agregamos al diccionario y al resultado
                        if tuple_keys not in clasificadores_dict:
                            clasificadores_dict[tuple_keys] = {
                                key: item[key] for key in keys
                            }
                            clasificadores_dict[tuple_keys]["items"] = []

                        clasificadores_dict[tuple_keys]["items"].append(item)

                    requeClasificadores = list(clasificadores_dict.values())

                    requerimiento_return["requeClasificadores"] = requeClasificadores

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

    def post(self, request: Request, anio, numero, tipo):

        try:
            requerimiento_new = request.data.get("requerimiento")

            login = request.user.username

            if int(numero) == 0:
                # Estoy creando un nuevo requerimiento
                numero = None
            else:
                # Estoy modificando el requerimiento
                removeNonRequiredItemsFromDatabase(requerimiento_new, login)


            fecha = requerimiento_new["D_reque_fecha"]

            obs = requerimiento_new["T_reque_obs"]
            tipo_gasto = requerimiento_new["C_tipogasto"]
            sf_dep = requerimiento_new["C_sf_dep"]
            libre = requerimiento_new["f_libre"]

            fecha = datetime.strptime(fecha, "%Y-%m-%d")

            my_xml = """<?xml version="1.0" encoding="utf-8" ?><root>"""

            for clasificador in requerimiento_new["requeClasificadores"]:
                for item in clasificador["items"]:
                    my_xml += """<Registro>"""
                    my_xml += """<Dato0>{}</Dato0>""".format(clasificador["C_depen"])
                    my_xml += """<Dato1>{}</Dato1>""".format(clasificador["C_secfun"])
                    my_xml += """<Dato2>{}</Dato2>""".format(item["C_bieser"])
                    my_xml += """<Dato3>{}</Dato3>""".format(item["C_biesertipo"])
                    my_xml += """<Dato4>{}</Dato4>""".format(item["Q_requedet_cant"])
                    my_xml += """<Dato5>{}</Dato5>""".format(item["Q_requedet_precio"])
                    my_xml += """<Dato6>{}</Dato6>""".format(item["C_item"])
                    my_xml += """<Dato7>{}</Dato7>""".format(clasificador["C_activpoi"])
                    my_xml += """<Dato8>{}</Dato8>""".format(clasificador["C_metapoi"])
                    my_xml += """<Dato9>{}</Dato9>""".format(clasificador["C_objpoi"])
                    my_xml += """<Dato10>{}</Dato10>""".format(clasificador["C_clapre"])
                    my_xml += """<Dato11>{}</Dato11>""".format(item["c_depen_aux"])
                    my_xml += """<Dato12>{}</Dato12>""".format(item["N_cnespec_desc"])
                    my_xml += """</Registro>"""

            my_xml += """</root>"""

            requerimiento = InsertRequeMyXML(
                {
                    "anipre": anio,
                    "numero": numero,
                    "fecha": fecha,
                    "obs": obs,
                    "tipogasto": tipo_gasto,
                    "biesertipo": tipo,
                    "sf_dep": sf_dep,
                    "my_xml": my_xml,
                    "user": login,
                    "libre": libre,
                    "depen": None,
                    "traba_dni": None,
                }
            )

            return Response(
                data={"message": "", "content": requerimiento[0]}, status=200
            )

        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        
    def delete(self, request: Request, anio, numero, tipo):
        try:
            observaciones = request.data.get("observaciones")
            login = request.user.username

            tabla = "REQUE_COMPRA" if tipo == "01" else "REQUE_SERVICIO"

            AnularDocumentos(tabla, anio, numero, observaciones, login)

            return Response(
                data={"message": "Requerimiento anulado correctamente"},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                data={"message": e.args, "content": None},
                status=400,
            )


def removeNonRequiredItemsFromDatabase(requerimiento_new, login):
    #  funcion que recibe como parametro los items de un requerimiento de bienes, y compara con los que actualmente estan en la base de datos, aquellos que esten en la base de datos pero no en el parametro recibido, los elimina de la base de datos
    anio = requerimiento_new["C_anipre"]
    numero = requerimiento_new["C_reque"]
    tipo = requerimiento_new["C_biesertipo"]

    requerimiento_new_format = []

    for clasificador in requerimiento_new["requeClasificadores"]:
        for item in clasificador["items"]:
            requerimiento_new_format.append(
                {
                    "C_anipre": requerimiento_new["C_anipre"],
                    "C_reque": requerimiento_new["C_reque"],
                    "C_secfun": clasificador["C_secfun"],
                    "C_depen": clasificador["C_depen"],
                    "C_biesertipo": item["C_biesertipo"],
                    "C_bieser": item["C_bieser"],
                    "C_item": item["C_item"],
                }
            )

    requerimientos_db = SelectRequeDetalle(anio, numero, tipo)

    for requerimiento_db in requerimientos_db:
        requerimiento_db_format = {
            "C_anipre": requerimiento_db["C_anipre"],
            "C_reque": requerimiento_db["C_reque"],
            "C_secfun": requerimiento_db["C_secfun"],
            "C_depen": requerimiento_db["C_depen"],
            "C_biesertipo": requerimiento_db["C_biesertipo"],
            "C_bieser": requerimiento_db["C_bieser"],
            "C_item": requerimiento_db["C_ITEM"],
        }

        if requerimiento_db_format not in requerimiento_new_format:
            #  eliminar de la base de datos
            DeleteRequeDetalle(requerimiento_db_format["C_anipre"], requerimiento_db_format["C_reque"], requerimiento_db_format["C_secfun"], requerimiento_db_format["C_depen"], requerimiento_db_format["C_biesertipo"], requerimiento_db_format["C_bieser"], requerimiento_db_format["C_item"], login)



class SelectSaldoPresupRequeController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:

            anio = request.query_params.get("anio")
            numero = request.query_params.get("numero")
            bie_ser_tipo = request.query_params.get("tipo")

            if anio and numero and bie_ser_tipo:
                requerimiento = SelectSaldoPresupReque(anio, numero, bie_ser_tipo)

                return Response(
                    data={"message": None, "content": requerimiento}, status=200
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
        

class SelectRequeFuentesController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:

            anio = request.query_params.get("anio")
            secfun = request.query_params.get("secfun")
            depen = request.query_params.get("depen")
            clasif = request.query_params.get("clasif")
            fecha = request.query_params.get("fecha", None)
            meta = request.query_params.get("meta", None)
            obj = request.query_params.get("obj", None)
            todo = request.query_params.get("todo", None)
            fuente = request.query_params.get("fuente", None)
            recurso = request.query_params.get("recurso", None)

            if anio and secfun and depen and clasif and fecha:
                saldos = RequeFuentes(anio, secfun, depen, clasif, fecha, meta, obj, todo, fuente, recurso)

                return Response(
                    data={"message": None, "content": saldos}, status=200
                )

            else:
                return Response(
                    data={
                        "message": "Debe de ingresar año, secuencia funcional, dependencia, clasificador y fecha buscada",
                        "content": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )        
        
class SelectSaldoPresupRequeItemController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):

        try:

            anio = request.query_params.get("anio")
            secfun = request.query_params.get("secfun")
            depen = request.query_params.get("depen")
            clasif = request.query_params.get("clasif")
            meta = request.query_params.get("meta")
            obj = request.query_params.get("obj")
            actividad = request.query_params.get("actividad")

            if anio and secfun and depen and clasif and meta and obj:
                saldos = SelectSaldoPresupRequeItem(anio, secfun, depen, clasif, meta, obj, actividad)

                return Response(
                    data={"message": None, "content": saldos}, status=200
                )

            else:
                return Response(
                    data={
                        "message": "Debe de ingresar año, secuencia funcional, dependencia, clasificador y fecha buscada",
                        "content": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )                
        
class RequePrecomprometerController(RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, anio, numero, tipo):

        try:

            sf_dep = request.data.get("C_sf_dep")
            dni = request.data.get("c_traba_dni")
            libre = request.data.get("f_libre")
            login = request.user.username
            fecha = datetime.now().date()

            my_xml = """<?xml version="1.0" encoding="utf-8" ?><root>"""

            
            for item in request.data.get("gastos"):
                my_xml += """<Registro>"""
                my_xml += """<Dato0>{}</Dato0>""".format(item["C_depen"])
                my_xml += """<Dato1>{}</Dato1>""".format(item["C_secfun"])
                my_xml += """<Dato2>{}</Dato2>""".format(item["C_clapre"])
                my_xml += """<Dato3>{}</Dato3>""".format(item["C_fuefin"])
                my_xml += """<Dato4>{}</Dato4>""".format(item["C_recurso"])
                my_xml += """<Dato5>{}</Dato5>""".format(item["total_precompromiso"])
                my_xml += """<Dato6>{}</Dato6>""".format(item["C_metapoi"])
                my_xml += """<Dato7>{}</Dato7>""".format(item["C_objpoi"])
                my_xml += """<Dato8>{}</Dato8>""".format(item["C_activpoi"])
                my_xml += """</Registro>"""

            my_xml += """</root>"""
        
            params = {
                "anipre": anio,
                "reque": numero,
                "biesertipo": tipo,
                "my_xml": my_xml,
                "fecha": fecha,
                "user": login,
                "depen": sf_dep,
                "traba_dni": dni,
                "libre": libre
            }

            precompromiso = PrecompromisoReque(params)

            return Response(
                data={"message": "", "content": precompromiso[0]}, status=200
            )

        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )        


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def RequeImprimirController(request, anio, numero, tipo):    
    try:

        if anio and numero and tipo:

            tipo_gasto = [
                {"1": "FUNCIONAMIENTO"},
                {"2": "INVERSION"},
                {"3": "NINGUNO"},
            ]
            
            requerimiento = SelectRequeById(anio, numero, tipo)

            if len(requerimiento) == 0:
                return Response(
                    data={"message": None, "content": {}}, status=200
                )
            
            requerimiento = requerimiento[0]

            login = request.user            
            
            fecha_print = datetime.now().strftime('%d/%m/%Y %I:%M:%S %p')            
            c_sf_dep = requerimiento["C_sf_dep"]

            field = "NUMERO"
            if c_sf_dep is None:
                requeSf_dep = SelectReque(anio, field, numero, tipo)
            else:
                requeSf_dep = SelectRequeSf_dep(anio, c_sf_dep, tipo, field, numero, None, None)
                            
            requeSf_dep = requeSf_dep[0]

            f_reque_estado = requeSf_dep["F_reque_estado"]
            C_exp = requeSf_dep["C_exp"]
            C_tipogasto = requeSf_dep["C_tipogasto"]
            D_reque_fecha = requeSf_dep["D_reque_fecha"]
            n_proceso = requeSf_dep.get("n_proceso", "") or ""            
            c_prosel = requeSf_dep.get("C_prosel", "") or ""
            q_reque_total = requeSf_dep.get("Q_REQUE_TOTAL", 0)
            n_observaciones = requeSf_dep.get("T_reque_obs", "") or ""
            
            tipo_certificacion = {}
            expediente_fase = {}
            n_tipcertif_desc = ""
            c_tipceruser= ""

            if f_reque_estado == "2":
                ciclo = "G"
                fase = "Q"
                secu = "0001"

                expediente_fase = SelectExpedienteFase(anio, C_exp, ciclo, fase, secu)

                if len(expediente_fase) > 0:
                    expediente_fase = expediente_fase[0]
                    c_tipcertif = expediente_fase.get("c_tipcertif", None)
                    n_tipcertif_desc = expediente_fase.get("n_tipcertif_desc", "")
                    c_tipceruser = expediente_fase.get("C_TipCerUser", "")
                    if c_tipcertif:
                        field = "CODIGO"
                        tipo_certificacion = SelectTipo_Certificacion(field, c_tipcertif)
                        if len(tipo_certificacion) > 0:
                            tipo_certificacion = tipo_certificacion[0]

            reque_gasto = ListaRequeGasto(anio, numero, C_tipogasto, tipo)

            lista_reque = ListaReque(anio, numero, tipo)

            reque_detalle_secfun = ""
            reque_detalle_depen = ""
            lista_reque_format = []

            for row_lista_reque in lista_reque:
                if reque_detalle_secfun != row_lista_reque["C_SECFUN"]:
                    lista_reque_format.append({
                        "C_secfun": row_lista_reque["C_SECFUN"],
                        "N_secfun_desc": row_lista_reque["N_METAPRESUP_DESC"],
                        "dependencias": []
                    }
                    )
                    reque_detalle_depen = ""

                if reque_detalle_depen != row_lista_reque["C_DEPEN"]:
                    lista_reque_format[-1]["dependencias"].append({
                        "C_depen": row_lista_reque["C_DEPEN"],
                        "N_depen_desc": row_lista_reque["N_DEPENDENCIA_DESC"],
                        "items": []
                    }
                    )

                lista_reque_format[-1]["dependencias"][-1]["items"].append({
                    "C_bieser": row_lista_reque["C_BIESER"],
                    "N_bieser_desc": row_lista_reque["N_BIESER_DESC"],
                    "N_unimed_desc": row_lista_reque["N_UNIMED_DESC"],
                    "Q_requedet_cant": row_lista_reque["Q_REQUEDET_CANT"],
                    "Q_requedet_precio": row_lista_reque["Q_REQUEDET_PRECIO"],
                    "Q_requedet_subtotal": row_lista_reque["Q_REQUEDET_SUBTOTAL"],
                    "N_cnespec_desc": row_lista_reque["N_cnespec_desc"]                    
                })

                reque_detalle_secfun = row_lista_reque["C_SECFUN"]
                reque_detalle_depen = row_lista_reque["C_DEPEN"]

            # ********************* INCIO HEADER PDF ********************* #
                
            
            
            template = get_template('reque-header.html')
            context = {"C_reque" : numero,
                       "C_exp" : C_exp, 
                       "N_tipo": "BIENES" if tipo == "01" else "SERVICIOS",
                       "D_reque_fecha": D_reque_fecha.strftime('%d/%m/%Y') if D_reque_fecha else None,
                        "N_tipogasto": tipo_gasto[int(C_tipogasto) - 1][C_tipogasto],
                        "N_proceso": n_proceso,
                        "C_prosel": c_prosel
                    }
            
            options = {
                'encoding': "UTF-8",                           
            }  

            page_header = template.render(context = context)
            header_template_path = os.path.join(settings.MEDIA_ROOT, 'reque-header' + str(uuid.uuid4()) + '.html')
            
            text_file = open(header_template_path, "w")            
            text_file.write(page_header)
            text_file.close()

            # ********************* INCIO FOOTER PDF ********************* #
            
            template = get_template('reque-footer.html')
            page_footer = template.render({"login": login, "fecha_print": fecha_print})
            footer_template_path = os.path.join(settings.MEDIA_ROOT, 'reque-footer' + str(uuid.uuid4()) + '.html')
            
            text_file = open(footer_template_path, "w")            
            text_file.write(page_footer)
            text_file.close()

            # ********************* INCIO MAIN PDF ********************* #
                            

            context = {"C_reque" : numero,
                       "C_exp" : C_exp, 
                       "N_tipo": "BIENES" if tipo == "01" else "SERVICIOS",
                       "D_reque_fecha": D_reque_fecha.strftime('%d/%m/%Y') if D_reque_fecha else None,
                        "N_tipogasto": tipo_gasto[int(C_tipogasto) - 1][C_tipogasto],
                        "N_proceso": n_proceso,
                        "C_prosel": c_prosel,
                        "lista_reque_format": lista_reque_format,
                        "Q_reque_total": q_reque_total,
                        "reque_gasto": reque_gasto,
                        "N_observaciones": n_observaciones.replace('\n', '<br>'),
                        "N_tipcertif_desc": n_tipcertif_desc,
                        "C_tipceruser": c_tipceruser,
                        "tipo": tipo,
                        "login": login,
                        "fecha_print": fecha_print,                        
                    }
            
  
            
            template = get_template('requerimiento.html')            
            html = template.render(context = context)    
            
            options = {
                'page-size': 'A4',
                'margin-top': '2.0in',
                'margin-right': '0.25in',
                'margin-bottom': '0.50in',
                'margin-left': '0.25in',
                'encoding': "UTF-8",                           
                'footer-html': footer_template_path,    
                'header-html': header_template_path,
                'footer-font-size':'7',
                'footer-right': 'Página [page] de [topage]',                
            }                    
                    
            file_generate = pdfkit.from_string(html, False, options=options)
            response = HttpResponse(file_generate, content_type="application/pdf")
            file_name_download = "requerimiento{}.pdf".format(numero)
            # response['Content-Disposition'] = "attachment; filename={}".format(file_name_download)
            response['Content-Disposition'] = "inline; filename={}".format(file_name_download)


            # ********************* FIN GENERANDO PDF ********************* #
            os.remove(header_template_path)
            os.remove(footer_template_path)


            return response

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