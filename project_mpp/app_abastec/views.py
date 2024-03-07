import json
from datetime import datetime

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
    SelectBBSSDisponibleOrden,
    InsertRequeMyXML,
    SelectRequeDetalle
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
                            actividad = {"C_activpoi": saldo[i]["C_activpoi"], "N_activpoi_desc": saldo[i]["N_activpoi_desc"], "C_depen": saldo[i]["C_depen"]  ,"clasificadores": []}
                            row["actividades"].append(actividad)

                        if clapre != saldo[i]["C_clapre"] or objpoi != saldo[i]["C_objpoi"] or metapoi != saldo[i]["C_metapoi"]:
                            clasificador = {"C_clapre": saldo[i]["C_clapre"], "C_objpoi": saldo[i]["C_objpoi"], "C_metapoi": saldo[i]["C_metapoi"], "saldos": [], "selecc": False}
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
                bienes_servicios = SelectBBSSDisponibleOrden(anio, sec_fun, cod_dep, bie_ser_tipo, file, valor)                

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
        
class RequerimientoController(RetrieveAPIView):
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

                    key_mapping = {'c_clapre': 'C_clapre', "C_ITEM": "C_item", "N_BIESER_DESC": "N_bieser_desc", "N_UNIMED_DESC": "N_unimed_desc"}
                    datalle_format = []

                    for item in detalle:
                        updated_json = {key_mapping.get(key, key): value for key, value in item.items()}
                        datalle_format.append(updated_json)

                    keys = ["C_clapre", "C_secfun", "C_depen", "C_activpoi", "C_objpoi", "C_metapoi"]
                    clasificadores_dict = {}

                    for item in datalle_format:
                        # Creamos una tupla con los valores de las claves que nos interesan
                        tuple_keys = tuple(item[key] for key in keys)
                        
                        # Si la tupla no está en el diccionario, la agregamos al diccionario y al resultado
                        if tuple_keys not in clasificadores_dict:
                            clasificadores_dict[tuple_keys] = {key: item[key] for key in keys}
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
            if int(numero) == 0:
                numero = None

            requerimiento = request.data.get("requerimiento") 

            fecha = requerimiento["D_reque_fecha"]
            obs = requerimiento["T_reque_obs"]
            tipo_gasto = requerimiento["C_tipogasto"]
            sf_dep = requerimiento["C_sf_dep"]
            login = request.user.username      
            libre = requerimiento["f_libre"]

            fecha = datetime.strptime(fecha, "%Y-%m-%d")
            
            my_xml = '''<?xml version="1.0" encoding="utf-8" ?><root>'''

            for clasificador in requerimiento["requeClasificadores"]:   
                for item in clasificador["items"]:                
                    my_xml += '''<Registro>'''
                    my_xml += '''<Dato0>{}</Dato0>'''.format(clasificador["C_depen"])
                    my_xml += '''<Dato1>{}</Dato1>'''.format(clasificador["C_secfun"])
                    my_xml += '''<Dato2>{}</Dato2>'''.format(item["C_bieser"])
                    my_xml += '''<Dato3>{}</Dato3>'''.format(item["C_biesertipo"])
                    my_xml += '''<Dato4>{}</Dato4>'''.format(item["Q_requedet_cant"])
                    my_xml += '''<Dato5>{}</Dato5>'''.format(item["Q_requedet_precio"])
                    my_xml += '''<Dato6>{}</Dato6>'''.format(item["C_item"])
                    my_xml += '''<Dato7>{}</Dato7>'''.format(clasificador["C_activpoi"])
                    my_xml += '''<Dato8>{}</Dato8>'''.format(clasificador["C_metapoi"])
                    my_xml += '''<Dato9>{}</Dato9>'''.format(clasificador["C_objpoi"])
                    my_xml += '''<Dato10>{}</Dato10>'''.format(clasificador["C_clapre"])
                    my_xml += '''<Dato11>{}</Dato11>'''.format(item["c_depen_aux"])
                    my_xml += '''<Dato12>{}</Dato12>'''.format(item["N_cnespec_desc"])
                    my_xml += '''</Registro>'''

            my_xml += '''</root>'''

            requerimiento = InsertRequeMyXML({
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
                "traba_dni": None
            
            })

            return Response(
                data={"message": "", "content": requerimiento[0]}, status=200
            )

        except Exception as e:
            return Response(
                data={"message": str(e), "content": None},
                status=status.HTTP_404_NOT_FOUND,
            )
        


        