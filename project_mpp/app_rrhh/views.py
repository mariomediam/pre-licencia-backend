import os
import calendar

from os import environ

from django.shortcuts import render
from django.template.loader import get_template

from rest_framework import status
from rest_framework.generics import UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.request import Request


from dotenv import load_dotenv

from app_rrhh.rrhh import SelectPlanillaBoleta, ListaPlanillaResumen, ListaBoletaPagoWeb, InsertBoletaCarpeta, UpdateBoletaCarpeta, DeleteBoletaCarpeta
from app_deploy.general.utilitarios import getMonthName


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

import pdfkit

# Create your views here.

class GenerateBoletasPdfController(UpdateAPIView):    
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        
        anio = request.data.get('anio')
        mes = request.data.get('mes')
        tipo = request.data.get('tipo')
        numero = request.data.get('numero')
        login = request.user.username
        
        if anio and mes and tipo and numero:

            boleta_pago = ListaBoletaPagoWeb(anio, mes, tipo, numero)

            if len(boleta_pago) > 0:

                try:
                    i=0
                    data = []
                    
                    InsertBoletaCarpeta(anio, mes, tipo, numero, 0, '', login)

                    # ******************** INICIO CREA DIRECTORIO ********************

                    BASE_DIR = environ.get('RUTA_BOLETAS_PAGO')                    

                    carpeta = BASE_DIR 

                    if not os.path.exists(carpeta + "\\" + str(anio)):
                        # Crear carpeta año
                        os.mkdir(carpeta + "\\" + str(anio))

                    carpeta += "\\" + str(anio)

                    month_name = getMonthName(mes)

                    if not os.path.exists(carpeta + "\\" + month_name):
                        # Crear carpeta mes
                        os.mkdir(carpeta + "\\" + month_name)
                    
                    carpeta += "\\" + month_name

                    nombre_planilla = boleta_pago[0]["n_tippla_nombre"].strip() + "-" + str(numero).zfill(2)                    

                    if not os.path.exists(carpeta + "\\" + nombre_planilla):
                        # Crear carpeta tipo y número de planilla
                        os.mkdir(carpeta + "\\" + nombre_planilla)
                    
                    carpeta += "\\" + nombre_planilla                    

                    # ******************** INICIO CREA ARCHIVOS ********************

                    while i < len(boleta_pago):

                        filepdf = str(boleta_pago[i]["d_ano"]) + str(boleta_pago[i]["d_mes"]) + str(boleta_pago[i]["c_tippla_id"]) + str(boleta_pago[i]["c_plani_nro"]) + boleta_pago[i]["c_traba_dni"] + '.pdf'
                        
                        c_traba_dni = boleta_pago[i]["c_traba_dni"]
                        n_nombre = boleta_pago[i]["n_nombre"]
                        d_traba_fecing = boleta_pago[i]["d_traba_fecing"]
                        n_cargo_nombre = boleta_pago[i]["n_cargo_nombre"]
                        n_depend_descripcion =boleta_pago[i]["n_depend_descripcion"]
                        n_traba_cuspp = boleta_pago[i]["n_traba_cuspp"]
                        n_traba_carseg = boleta_pago[i]["n_traba_carseg"]
                        n_traba_carseg = boleta_pago[i]["n_traba_carseg"]
                        n_traba_ctabco = boleta_pago[i]["n_traba_ctabco"]
                        q_plani_dias = boleta_pago[i]["q_plani_dias"]
                        q_traba_plaza = boleta_pago[i]["q_traba_plaza"]
                        n_categ_nombre = boleta_pago[i]["n_categ_nombre"]
                        n_conlab_nombre = boleta_pago[i]["n_conlab_nombre"]
                        n_tser_reco = boleta_pago[i]["n_tser_reco"]
                        n_boleta_titulo = boleta_pago[i]["n_boleta_titulo"]

                        array_ingresos = []
                        array_descuentos = []
                        array_aportes = []
                        total_ingresos = 0.00
                        total_descuentos = 0.00
                        total_aportes = 0.00

                        while i < len(boleta_pago) and c_traba_dni == boleta_pago[i]["c_traba_dni"]:

                            if boleta_pago[i]["c_tiprub_id"]==1:
                                array_ingresos.append({"c_rubro" : boleta_pago[i]["c_rubro"], "n_rubro_abrev" : boleta_pago[i]["n_rubro_abrev"], "q_pladet_monto" : boleta_pago[i]["q_pladet_monto"]})
                                total_ingresos = total_ingresos + float(boleta_pago[i]["q_pladet_monto"])

                            if boleta_pago[i]["c_tiprub_id"]==2:
                                array_descuentos.append({"c_rubro" : boleta_pago[i]["c_rubro"], "n_rubro_abrev" : boleta_pago[i]["n_rubro_abrev"], "q_pladet_monto" : boleta_pago[i]["q_pladet_monto"]})
                                total_descuentos = total_descuentos + float(boleta_pago[i]["q_pladet_monto"])

                            if boleta_pago[i]["c_tiprub_id"]==3:
                                array_aportes.append({"c_rubro" : boleta_pago[i]["c_rubro"], "n_rubro_abrev" : boleta_pago[i]["n_rubro_abrev"], "q_pladet_monto" : boleta_pago[i]["q_pladet_monto"]})
                                total_aportes = total_aportes + float(boleta_pago[i]["q_pladet_monto"])

                            i=i+1

                        context = {"c_traba_dni" : c_traba_dni,
                        "n_nombre" : n_nombre,
                        "d_traba_fecing" : d_traba_fecing, 
                        "n_cargo_nombre" : n_cargo_nombre,
                        "n_depend_descripcion" : n_depend_descripcion,
                        "n_traba_cuspp" : n_traba_cuspp,
                        "n_traba_carseg" : n_traba_carseg,
                        "n_traba_carseg" : n_traba_carseg,
                        "n_traba_ctabco" : n_traba_ctabco,
                        "q_plani_dias" : q_plani_dias,
                        "q_traba_plaza" : q_traba_plaza,
                        "n_categ_nombre" : n_categ_nombre,
                        "n_conlab_nombre" : n_conlab_nombre,
                        "n_tser_reco" : n_tser_reco,
                        "n_boleta_titulo" : n_boleta_titulo,
                        "ingresos" : array_ingresos,
                        "descuentos" : array_descuentos,
                        "aportes" : array_aportes,
                        "total_ingresos" : round(total_ingresos,2),
                        "total_descuentos" : round(total_descuentos,2),
                        "total_aportes" : round(total_aportes,2),
                        "importe_liquido" : round(total_ingresos - total_descuentos,2)}
                    
                        template = get_template('boleta.html')
                        html = template.render(context = context)                        
                    
                        file_path = carpeta  + "\\" +  filepdf

                        pdfkit.from_string(html, file_path)

                    UpdateBoletaCarpeta(anio, mes, tipo, numero, 1, carpeta, login)
                
                    return Response(data={
                        "message":"Boletas generadas con exito en carpeta: " + carpeta
                        }, status=status.HTTP_200_OK)
                    pass

                except Exception as e:
                    DeleteBoletaCarpeta(anio, mes, tipo, numero, login)
                    return Response(data={
                        "message":e.args,
                        }, status=status.HTTP_400_BAD_REQUEST)
                
            else:
                return Response(data={
                    "message":"No se encontraron datos"
                    }, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={
                "message":"Error al generar boleta"
                }, status=status.HTTP_400_BAD_REQUEST)  
        

# Create your views here.
class SelectPlanillaBoletaController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        anio = request.query_params.get('anio')
        mes = request.query_params.get('mes')
        tipo = request.query_params.get('tipo')
        numero = request.query_params.get('numero')


        if anio and mes:            
            planillas = SelectPlanillaBoleta(anio, mes, tipo, numero)
            
            return Response(data = {
            "message":None,
            "content":planillas
            }, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar año y mes a consultar"
                }, status=status.HTTP_404_NOT_FOUND)        
        

# Create your views here.
class ListaPlanillaResumenController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        anio = request.query_params.get('anio')
        mes = request.query_params.get('mes')
        tipo = request.query_params.get('tipo')
        numero = request.query_params.get('numero')

        if anio and mes:            
            planilla = ListaPlanillaResumen(anio, mes, tipo, numero)
            
            return Response(data = {
            "message":None,
            "content":planilla
            }, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar año, mes, tipo y numero a consultar"
                }, status=status.HTTP_404_NOT_FOUND)                