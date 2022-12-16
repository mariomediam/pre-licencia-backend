from django.shortcuts import render
from django.db import transaction
from rest_framework.generics import RetrieveAPIView, ListAPIView, UpdateAPIView, CreateAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status, mixins
from datetime import date
from app_contribuyente.contribuyente import BuscarContribNombre, BuscarContribCodigo, ConsultaContribCodigo, ConsultaDocumentoNumero, ListarTipoContribuyente, ConsultaTipoLugar, ConsultaSectores, ConsultaLugaresGeneral, ConsultaTipLugCodigo, ConsultaTelefonoCont, ConsultaDocumentoCont, ConsultaDirElectCont, ConsultaNacionalidadCont, separaNombre, ConsultaCallesGeneral, ListarTipDoc, ConsultaDocumentoTipoNro, ConsultaTiposTelefono, ListarTipoNacion, UpdateContribuyente, DeleteDocumentoContrib, EnviarDocumentoContrib, DeleteTelefonoContrib, EnviarTelefonoContrib, DeleteDirElectContrib, EnviarDirElectContrib, DeleteNacionalidadContrib, EnviarNacionalidadContrib, InsertContribuyente, generaCorrelativoCodContribuyente

from app_deploy.general.paginations import CustomPagination

# Create your views here.

class BuscarContribNombreController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        nombre_contrib = request.query_params.get('nombre')        

        if nombre_contrib:            
            contribuyente = BuscarContribNombre(nombre_contrib)
            return Response(data={
                    "message":None,
                    "content": contribuyente
                }, status=status.HTTP_200_OK)
            # return Response({'data': contribuyente}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar nombre a buscar"
                }, status=status.HTTP_404_NOT_FOUND)


class BuscarContribCodigoController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo_contrib = request.query_params.get('codigo')        

        if codigo_contrib:            
            contribuyente = BuscarContribCodigo(codigo_contrib)
            
            if len(contribuyente) == 1:
                separa_nombre = separaNombre(contribuyente[0]["Identificación"])
                contribuyente[0].update(separa_nombre)
                
            return Response(data={
                    "message":None,
                    "content": contribuyente
                }, status=status.HTTP_200_OK)
            # return Response({'data': contribuyente}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)


class ConsultaContribCodigoController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo_contrib = request.query_params.get('codigo')        

        if codigo_contrib:            
            contribuyente = ConsultaContribCodigo(codigo_contrib)
            return Response(data={
                    "message":None,
                    "content": contribuyente
                }, status=status.HTTP_200_OK)
            # return Response({'data': contribuyente}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                


class ConsultaDocumentoNumeroController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):    
        numero_documento = request.query_params.get('numero')        
        if numero_documento:            
            documento = ConsultaDocumentoNumero(numero_documento)
            return Response(data={
                    "message":None,
                    "content": documento
                }, status=status.HTTP_200_OK)
            # return Response({'data': documento}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                


class ListarTipoContribuyenteController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        documento = ListarTipoContribuyente()
        return Response(data={
                    "message":None,
                    "content": documento
                }, status=status.HTTP_200_OK)
        # return Response({'data': documento}, status=status.HTTP_200_OK)


class ConsultaTipoLugarController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        tipo_lugar = ConsultaTipoLugar()
        return Response(data={
                    "message":None,
                    "content": tipo_lugar
                }, status=status.HTTP_200_OK)
        # return Response({'data': tipo_lugar}, status=status.HTTP_200_OK)


class ConsultaSectoresController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        sectores = ConsultaSectores()
        return Response(data={
                    "message":None,
                    "content": sectores
                }, status=status.HTTP_200_OK)
        # return Response({'data': sectores}, status=status.HTTP_200_OK)


class ConsultaLugarGeneralController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):    
        codigo = request.query_params.get('codigo', '')
        nombre = request.query_params.get('nombre', '')
        tipo_lugar = request.query_params.get('tiplug', '')
        sector = request.query_params.get('sector', '')
        calificacion = request.query_params.get('calif', '')
        dpto = request.query_params.get('dpto', '')
        prov = request.query_params.get('prov', '')
        dist = request.query_params.get('dist', '')

        lugar = ConsultaLugaresGeneral(codigo, nombre, tipo_lugar, sector, calificacion, dpto, prov, dist)

        return Response(data={
                    "message":None,
                    "content": lugar
                }, status=status.HTTP_200_OK)
        # return Response({'data': lugar}, status=status.HTTP_200_OK)
        

class ConsultaTipLugController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo = request.query_params.get('codigo')        

        if codigo:            
            tipo_lugar = ConsultaTipLugCodigo(codigo)
            return Response(data={
                    "message":None,
                    "content": tipo_lugar
                }, status=status.HTTP_200_OK)
            # return Response({'data': tipo_lugar}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo a buscar"
                }, status=status.HTTP_404_NOT_FOUND)   
        

class BuscarContribPaginationController(ListAPIView,mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]    
    pagination_class = CustomPagination    
        
    def get(self, request: Request):

        nombre_contrib = request.query_params.get('nombre')        
        codigo_contrib = request.query_params.get('codigo')

        if nombre_contrib or codigo_contrib:

            contribuyente = BuscarContribCodigo(codigo_contrib) if codigo_contrib else  BuscarContribNombre(nombre_contrib)
              
            return self.get_paginated_response(self.paginate_queryset(contribuyente))        
        
        else:
             return Response(data={
                    "message":"Debe de ingresar nombre o código a buscar"
                }, status=status.HTTP_404_NOT_FOUND)
        
class ConsultaTelefonoContController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo = request.query_params.get('codigo')        

        if codigo:            
            telefono = ConsultaTelefonoCont(codigo)
            return Response(data={
                    "message":None,
                    "content": telefono
                }, status=status.HTTP_200_OK)
            # return Response({'data': telefono}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo de contribuyente a buscar"
                }, status=status.HTTP_404_NOT_FOUND)           
        

class ConsultaDocumentoContController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo = request.query_params.get('codigo')        

        if codigo:            
            documento = ConsultaDocumentoCont(codigo)
            return Response(data={
                    "message":None,
                    "content": documento
                }, status=status.HTTP_200_OK)
            # return Response({'data': documento}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo de contribuyente a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                   
        
class ConsultaDirElectContController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo = request.query_params.get('codigo')        

        if codigo:            
            dir_elect = ConsultaDirElectCont(codigo)
            return Response(data={
                    "message":None,
                    "content": dir_elect
                }, status=status.HTTP_200_OK)
            # return Response({'data': dir_elect}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo de contribuyente a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                   
        
class ConsultaNacionalidadController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        codigo = request.query_params.get('codigo')        

        if codigo:            
            nacionalidad = ConsultaNacionalidadCont(codigo)
            return Response(data={
                    "message":None,
                    "content": nacionalidad
                }, status=status.HTTP_200_OK)
            # return Response({'data': nacionalidad}, status=status.HTTP_200_OK)

        else:
             return Response(data={
                    "message":"Debe de ingresar codigo de contribuyente a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                           

class ConsultaLugarGeneralPaginationController(ListAPIView,mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]    
    pagination_class = CustomPagination    
        
    def get(self, request: Request):

        codigo = request.query_params.get('codigo', '')
        nombre = request.query_params.get('nombre', '')
        tipo_lugar = request.query_params.get('tiplug', '')
        sector = request.query_params.get('sector', '')
        calificacion = request.query_params.get('calif', '')
        dpto = request.query_params.get('dpto', '')
        prov = request.query_params.get('prov', '')
        dist = request.query_params.get('dist', '')

        if len(codigo) > 0 or len(nombre) > 0 or len(tipo_lugar) > 0 or len(sector) > 0 or len(calificacion) > 0 or len(dpto) > 0 or len(prov) > 0 or len(dist) > 0:
            lugar = ConsultaLugaresGeneral(codigo, nombre, tipo_lugar, sector, calificacion, dpto, prov, dist)

            return self.get_paginated_response(self.paginate_queryset(lugar))        
        
        else:
             return Response(data={
                    "message":"Debe de ingresar valor a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                

class ConsultaCalleGeneralController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):    
        codigo = request.query_params.get('codigo', '')
        nombre = request.query_params.get('nombre', '')

        if len(codigo) > 0 or len(nombre) > 0:
            calle = ConsultaCallesGeneral(codigo, nombre)
        
            return Response(data={
                        "message":None,
                        "content": calle
                    }, status=status.HTTP_200_OK)        
        else:
             return Response(data={
                    "message":"Debe de ingresar valor a buscar"
                }, status=status.HTTP_404_NOT_FOUND)
        

class ConsultaCalleGeneralPaginationController(ListAPIView,mixins.ListModelMixin):
    permission_classes = [IsAuthenticated]    
    pagination_class = CustomPagination    
        
    def get(self, request: Request):

        codigo = request.query_params.get('codigo', '')
        nombre = request.query_params.get('nombre', '')

        if len(codigo) > 0 or len(nombre) > 0:
            calle = ConsultaCallesGeneral(codigo, nombre)

            return self.get_paginated_response(self.paginate_queryset(calle))        
        
        else:
             return Response(data={
                    "message":"Debe de ingresar valor a buscar"
                }, status=status.HTTP_404_NOT_FOUND)                       


class ListarTipoDocumentoController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        tipo_documento = ListarTipDoc()
        return Response(data={
                    "message":None,
                    "content": tipo_documento
                }, status=status.HTTP_200_OK)
        

class ConsultaDocumentoTipoNroController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):    
        tipo = request.query_params.get('tipo', '')
        numero = request.query_params.get('numero', '')                

        if len(tipo) > 0 and len(numero) > 0:
            documento_nro = ConsultaDocumentoTipoNro(tipo, numero)
        
            return Response(data={
                        "message":None,
                        "content":documento_nro
                    }, status=status.HTTP_200_OK)        
        else:
             return Response(data={
                    "message":"Debe de ingresar tipo de documento y numero de documento"
                }, status=status.HTTP_404_NOT_FOUND)


class ConsultaTiposTelefonoController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        tipo_telefono = ConsultaTiposTelefono()
        return Response(data={
                    "message":None,
                    "content": tipo_telefono
                }, status=status.HTTP_200_OK)                


class ListarTipoNacionController(RetrieveAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):        
        nacion = ListarTipoNacion()
        return Response(data={
                    "message":None,
                    "content": nacion
                }, status=status.HTTP_200_OK)      


class UpdateContribuyenteAllController(UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, cod_cont):
        try:
            with transaction.atomic():             
                nombre = request.data.get("nombreCompleto")
                tipo_contrib = request.data.get("tipoContrib")
                cod_lugar = request.data.get("codigoLugar")
                cod_calle = request.data.get("codigoCalle")
                direc_nro = request.data.get("direccNro", "")
                direc_piso = request.data.get("direccPiso", "")
                direc_mzna = request.data.get("direccMzna", "")
                direc_lote = request.data.get("direccLote", "")
                direc_dpto = request.data.get("direccDpto", "")
                direc_adic = request.data.get("direccAdic", "")
                fec_registro = date.today()
                responsable = request.data.get("responsable")
                motivo = request.data.get("observ", "")
                profesion = request.data.get("profesion", "")
                homonimia = request.data.get("homonimia", "")
                cod_ant_contrib = request.data.get("codAntContrib", "")
                sexo = request.data.get("sexo")
                fec_nacimiento = request.data.get("fecNac", "1900-01-01 00:00:00")
                cod_inmueble = request.data.get("codInmueble", "")
                documentos = request.data.get("documentos")
                telefonos = request.data.get("telefonos")
                emails = request.data.get("emails")
                naciones = request.data.get("naciones")

                UpdateContribuyente(cod_cont, nombre, tipo_contrib, cod_lugar, cod_calle, direc_nro, direc_piso, direc_mzna, direc_lote, direc_dpto, direc_adic, fec_registro, responsable, motivo, profesion, homonimia, cod_ant_contrib, sexo, fec_nacimiento, cod_inmueble)      

                # ACTUALIZANDO DOCUMENTOS

                DeleteDocumentoContrib(cod_cont)

                cadena_documentos = ""

                for documento in documentos:
                    cadena_documentos += '{}~~{}~~NN~~'.format(documento["CodDoc"].strip(), documento["Número"].strip())
                    
                if len(cadena_documentos) > 0:
                    EnviarDocumentoContrib(cod_cont, cadena_documentos)

                # ACTUALIZANDO TELEFONOS

                DeleteTelefonoContrib(cod_cont)

                cadena_telefonos = ""

                for telefono in telefonos:
                    cadena_telefonos += '{}~~{}~~NN~~'.format(telefono["Número"].strip(), telefono["TipTel"].strip())

                if len(cadena_telefonos) > 0:
                    EnviarTelefonoContrib(cod_cont, cadena_telefonos)

                # ACTUALIZANDO EMAILS

                DeleteDirElectContrib(cod_cont)

                cadena_emails = ""

                for email in emails:
                    cadena_emails += '{}~~NN~~'.format(email["Dirección_Electrónica"].strip())

                if len(cadena_emails) > 0:
                    EnviarDirElectContrib(cod_cont, cadena_emails)

                # ACTUALIZANDO NACIONALIDAD

                DeleteNacionalidadContrib(cod_cont)

                cadena_nacionalidad = ""

                for nacionalidad in naciones:
                    cadena_nacionalidad += '{}~~{}~~NN~~'.format(nacionalidad["Codigo"].strip(), nacionalidad["Gentilicio"].strip())

                print(cadena_nacionalidad)
                    
                if len(cadena_nacionalidad) > 0:
                    EnviarNacionalidadContrib(cod_cont, cadena_nacionalidad)

                return Response(data={
                            'message': 'Registro actualizado con exito',
                            'content': None
                        }, status=status.HTTP_201_CREATED)
        except Exception as e:
                return Response(data={
                    'message': e.args,
                    'content': None
                }, status=400)


class InsertContribuyenteAllController(CreateAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request, cod_cont):
        try:
            with transaction.atomic():             
                nombre = request.data.get("nombreCompleto")
                tipo_contrib = request.data.get("tipoContrib")
                tipo_docum = request.data.get("tipoDocum")
                cod_lugar = request.data.get("codigoLugar")
                cod_calle = request.data.get("codigoCalle")
                direc_nro = request.data.get("direccNro", "")
                direc_piso = request.data.get("direccPiso", "")
                direc_mzna = request.data.get("direccMzna", "")
                direc_lote = request.data.get("direccLote", "")
                direc_dpto = request.data.get("direccDpto", "")
                direc_adic = request.data.get("direccAdic", "")
                fec_registro = date.today()
                responsable = request.data.get("responsable")
                motivo = request.data.get("observ", "")
                profesion = request.data.get("profesion", "")
                homonimia = request.data.get("homonimia", "")
                cod_ant_contrib = request.data.get("codAntContrib", "")
                sexo = request.data.get("sexo")
                fec_nacimiento = request.data.get("fecNac", "1900-01-01 00:00:00")
                cod_inmueble = request.data.get("codInmueble", "")
                placa = request.data.get("placa", "")
                papeleta = request.data.get("papeleta", "")
                documentos = request.data.get("documentos")
                telefonos = request.data.get("telefonos")
                emails = request.data.get("emails")
                naciones = request.data.get("naciones")

                cod_cont = cod_cont.strip()

                InsertContribuyente(cod_cont, cod_ant_contrib, nombre, tipo_contrib, tipo_docum, cod_lugar, cod_calle, direc_nro, direc_piso, direc_mzna, direc_lote, direc_dpto, direc_adic, fec_registro, responsable, motivo, homonimia, profesion, sexo, fec_nacimiento, placa, papeleta, cod_inmueble)      

                # ACTUALIZANDO DOCUMENTOS

                cadena_documentos = ""

                for documento in documentos:
                    documentos_existentes = ConsultaDocumentoTipoNro(documento["CodDoc"].strip(), documento["Número"].strip())                    
                    if len(documentos_existentes) > 0:
                        for documento_existente in documentos_existentes:
                            if documento_existente["C002Cod_Cont"].strip() != cod_cont:
                                raise Exception("El documento {} ya existe en el contribuyente {} {}".format(documento_existente["C002Num_Doc"].strip(), documento_existente["C002Cod_Cont"].strip(), documento_existente["C001Nombre"].strip()) )                                
                    else:
                        cadena_documentos += '{}~~{}~~NN~~'.format(documento["CodDoc"].strip(), documento["Número"].strip())
                    
                if len(cadena_documentos) > 0:
                    EnviarDocumentoContrib(cod_cont, cadena_documentos)

                # ACTUALIZANDO TELEFONOS
                
                cadena_telefonos = ""

                for telefono in telefonos:
                    cadena_telefonos += '{}~~{}~~NN~~'.format(telefono["Número"].strip(), telefono["TipTel"].strip())

                if len(cadena_telefonos) > 0:
                    EnviarTelefonoContrib(cod_cont, cadena_telefonos)

                # ACTUALIZANDO EMAILS

                cadena_emails = ""

                for email in emails:
                    cadena_emails += '{}~~NN~~'.format(email["Dirección_Electrónica"].strip())

                if len(cadena_emails) > 0:
                    EnviarDirElectContrib(cod_cont, cadena_emails)

                # ACTUALIZANDO NACIONALIDAD                

                cadena_nacionalidad = ""

                naciones_existentes = ConsultaNacionalidadCont(cod_cont)

                # VALIDO QUE LA NACIONALIDAD NO EXISTA PREVIAMENTE EN LA BD
                for nacionalidad in naciones:
                    if len(naciones_existentes) > 0 and len(list(filter(lambda naciones_existentes: naciones_existentes['Codigo'] == nacionalidad["Codigo"].strip(), naciones_existentes))) == 0:                        
                        cadena_nacionalidad += '{}~~{}~~NN~~'.format(nacionalidad["Codigo"].strip(), nacionalidad["Gentilicio"].strip())

                if len(cadena_nacionalidad) > 0:
                    EnviarNacionalidadContrib(cod_cont, cadena_nacionalidad)

                return Response(data={
                            'message': 'Registro agregado con exito',
                            'content': None
                        }, status=status.HTTP_201_CREATED)
        except Exception as e:
                return Response(data={
                    'message': e.args,
                    'content': None
                }, status=400)

                
class generaCorrelativoCodContribuyenteController(ListCreateAPIView):    
    permission_classes = [IsAuthenticated]

    def get(self, request: Request):
        
        cod_contribuyente = generaCorrelativoCodContribuyente()
        return Response(data={
                "message":None,
                "content": cod_contribuyente
            }, status=status.HTTP_200_OK)
