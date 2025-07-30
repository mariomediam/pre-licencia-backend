import os
import logging
import time
import base64
import json
import requests
from playwright.sync_api import sync_playwright
from typing import Optional, Dict, Any
from django.core.cache import cache

# Configurar logging
logger = logging.getLogger(__name__)

URL_LOGIN = "https://apps.mef.gob.pe/weblanding/#/landing"
TOKEN_REFRESH_THRESHOLD = 3 * 60  # 3 minutos antes de expirar

def decode_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Decodifica un token JWT sin verificar la firma
    """
    try:
        # Dividir el token en partes
        parts = token.split('.')
        if len(parts) != 3:
            return None
        
        # Decodificar el payload (segunda parte)
        payload = parts[1]
        # Agregar padding si es necesario
        payload += '=' * (4 - len(payload) % 4)
        
        # Decodificar de base64
        decoded_bytes = base64.urlsafe_b64decode(payload)
        decoded_str = decoded_bytes.decode('utf-8')
        
        # Parsear JSON
        return json.loads(decoded_str)
    except Exception as e:
        logger.error(f"Error al decodificar token JWT: {e}")
        return None

def get_token_expiration_time(token: str) -> Optional[int]:
    """
    Obtiene el tiempo de expiración de un token JWT
    """
    try:
        decoded = decode_jwt_token(token)
        if decoded and 'exp' in decoded:
            return decoded['exp']
        return None
    except Exception as e:
        logger.error(f"Error al obtener expiración del token: {e}")
        return None

def calculate_token_duration(token: str) -> Optional[int]:
    """
    Calcula la duración en segundos de un token JWT
    """
    try:
        decoded = decode_jwt_token(token)
        if decoded and 'exp' in decoded and 'iat' in decoded:
            return decoded['exp'] - decoded['iat']
        return None
    except Exception as e:
        logger.error(f"Error al calcular duración del token: {e}")
        return None

class SIAFTokenManager:

    def acquire_get_tokens_lock(self) -> bool:
        """
        Adquiere un lock para evitar múltiples logins simultáneos
        """
        try:            
            return cache.add(self.get_tokens_lock_key(), True, timeout=60)  # 60 segundos de lock
        except Exception as e:
            logger.error(f"Error al adquirir login lock: {e}")
            return False
    
    def release_get_tokens_lock(self) -> bool:
        """
        Libera el lock de login
        """
        try:            
            cache.delete(self.get_tokens_lock_key())
            return True
        except Exception as e:
            logger.error(f"Error al liberar login lock: {e}")
            return False
        
    def get_tokens_lock_key(self):
        """
        Retorna la clave del lock para evitar múltiples logins simultáneos
        """
        return "get_tokens_lock_key"
    
    def is_lock_active(self):
        """
        Verifica si el lock está activo (True) o inactivo (False)
        """
        try:
            return cache.get("get_tokens_lock_key", False)
        except Exception as e:
            logger.error(f"Error al verificar si el lock está activo: {e}")
            return False


    def login_siaf(self, username, password):
        try:
            # return 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJBeGxPdUtBVjBMN0xCa2k5VHhTcmxCaE92QUZzdzNCQjF3RWRfQmlXaGdJIn0.eyJleHAiOjE3NTEzMDM4MTQsImlhdCI6MTc1MTMwMDIxNCwiYXV0aF90aW1lIjoxNzUxMzAwMjEyLCJqdGkiOiI2MzZkOGRjYy05NDJjLTRiYjUtODVlMC00Yjk0MTJhMmI0ZDMiLCJpc3MiOiJodHRwczovL2F1dGhvcml6ZS5tZWYuZ29iLnBlL2F1dGgvcmVhbG1zL21lZiIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJmOjM2MGVjNWEwLTBlMjctNDM2OS04NzgxLTAwYzg4ZjMzMzc1MzowMjg5NzA0MSIsInR5cCI6IkJlYXJlciIsImF6cCI6Imp3dENsaWVudCIsInNlc3Npb25fc3RhdGUiOiJkMDVlNzdjNy0yOTZiLTQ0NjMtYmI0Ny0xZjViNzZkODJlNDYiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHJlYWQgd3JpdGUgcHJvZmlsZSIsInNpZCI6ImQwNWU3N2M3LTI5NmItNDQ2My1iYjQ3LTFmNWI3NmQ4MmU0NiIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiYXBlbGxpZG9wYXRlcm5vIjoiTUVESU5BIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiMDI4OTcwNDEiLCJnaXZlbl9uYW1lIjoiTUFSSU8gQUxFWEFOREVSIiwibm9tYnJlIjoiTUFSSU8gQUxFWEFOREVSIiwibm9tYnJldXN1YXJpbyI6Ik1BUklPIEFMRVhBTkRFUiBNRURJTkEgTUFSUVVFWiIsInVuaWRhZGVqZWN1dG9yYSI6IjMwMTUyOSIsImVudGlkYWQiOiJNVU5JQ0lQQUxJREFEIFBST1ZJTkNJQUwgREUgUElVUkEiLCJhcGVsbGlkb21hdGVybm8iOiJNQVJRVUVaIiwibmFtZSI6Ik1BUklPIEFMRVhBTkRFUiBNRURJTkEgTUFSUVVFWiIsImZhbWlseV9uYW1lIjoiTUVESU5BIE1BUlFVRVoiLCJ0aXBvdW5pZGFkIjoiTSIsInVzZXJuYW1lIjoiMDI4OTcwNDEifQ.oB5P9WRn7cw3cJBM-N3aRsL0S_XAcEYVDZspEU3K9c_cK9Z9fUuQa6vsAYXB_-Be2SvCiLZA8cev-I9Ukwi_QqokWe-_vNueYErocVWPqu3jqLEHTNRdcThZ60Qo93X2Pawgn87uhtdD3OEYjKDwIl_TXU6w6IONJep38VdcsgcbopBO2H5_e7Cz0oTPO9urSHjyJKVbBtxZ_ADqzDL8ywDWS98o1GfRDxlMwiSmzjD5vbjzECY2rsJXHKWEhLvamCQwlQsndyksqnvddnea1IyDvqyOQaGKn47L0YwQd1NUAl29ZV-BaXdWQvBrKlo9VHrQ-2x0fuzKkt17HIXYfQ', 'eyJhbGciOiJIUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICI2NjU2YzA0ZS0zZWI4LTQ4ODYtYTcxYi03ZGIxY2M1NzcyOTQifQ.eyJleHAiOjE3NTEzMDIwMTQsImlhdCI6MTc1MTMwMDIxNCwianRpIjoiNDA1MmJjMGMtZTc5Ni00NzdiLTk3ODMtMzc4ZmU3ODQ2MzMxIiwiaXNzIjoiaHR0cHM6Ly9hdXRob3JpemUubWVmLmdvYi5wZS9hdXRoL3JlYWxtcy9tZWYiLCJhdWQiOiJodHRwczovL2F1dGhvcml6ZS5tZWYuZ29iLnBlL2F1dGgvcmVhbG1zL21lZiIsInN1YiI6ImY6MzYwZWM1YTAtMGUyNy00MzY5LTg3ODEtMDBjODhmMzMzNzUzOjAyODk3MDQxIiwidHlwIjoiUmVmcmVzaCIsImF6cCI6Imp3dENsaWVudCIsInNlc3Npb25fc3RhdGUiOiJkMDVlNzdjNy0yOTZiLTQ0NjMtYmI0Ny0xZjViNzZkODJlNDYiLCJzY29wZSI6ImVtYWlsIHJlYWQgd3JpdGUgcHJvZmlsZSIsInNpZCI6ImQwNWU3N2M3LTI5NmItNDQ2My1iYjQ3LTFmNWI3NmQ4MmU0NiJ9.lvhDolZThnW6ZaQEps-L5Fs3Omnb-PB8TqWIGmKwT4A'
            
            print(" ********** 1 **********")
            
            with sync_playwright() as playwright: 
                print(" ********** 2 **********")
                browser = playwright.chromium.launch()   
                print(" ********** 3 **********")
                context = browser.new_context()  
                print(" ********** 4 **********")
                page = context.new_page()
                print(" ********** 5 **********")

                # Variable para almacenar el token            
                refresh_token = None
                access_token = None

                # Función para interceptar las respuestas
                def handle_response(response):
                    nonlocal refresh_token, access_token
                    print(" ********** 6 **********")
                    if "authorize.mef.gob.pe/auth/realms/mef/protocol/openid-connect/token" in response.url:  # Verifica si es la URL de la API de login
                        try:
                            print(" ********** 7 **********")
                            data = response.json()                        
                            print(" ********** 8 **********")
                            refresh_token = data.get('refresh_token')
                            print(" ********** 9 **********")
                            access_token = data.get('access_token')
                        except Exception as e:
                            print(" ********** 10 **********")
                            print("Error al procesar la respuesta:", e)

                # Escucha las respuestas
                print(" ********** 11 **********")
                page.on("response", handle_response)
                print(" ********** 12 **********")
                page.goto(URL_LOGIN)      
                print(" ********** 13 **********")
                time.sleep(3)
                print(" ********** 14 **********")
                page.click("text='SIAF'")
                print(" ********** 15 **********")

                page.wait_for_load_state('networkidle') 
                print(" ********** 16 **********")
                page.fill("#username", os.environ.get('SIAFWEB_USERNAME'))
                print(" ********** 17 **********")
                page.fill("#password", os.environ.get('SIAFWEB_PASSWORD'))
                print(" ********** 18 **********")
                time.sleep(7)
                page.click("#kc-login")
                print(" ********** 19 **********")
                page.wait_for_load_state('networkidle') 
                print(" ********** 20 **********")
                title = page.title()
                print(" ********** 21 **********")
                
            
                # Captura la pantalla
                # page.screenshot(path="screenshot.png")

                # Cierra el navegador
                browser.close()
                return access_token, refresh_token
        
        except Exception as e:
            print(f"Error: {e}")
            return e
        

    def save_tokens(self, access_token, refresh_token):
        try:            
            current_time = time.time()
            expires_in = calculate_token_duration(access_token)
            refresh_expires_in = calculate_token_duration(refresh_token)
            timeout = refresh_expires_in             

            tokens = {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "access_token_expires_at": current_time + expires_in,
                "refresh_token_expires_at": current_time + refresh_expires_in,
                "expires_in": expires_in,
                "refresh_expires_in": refresh_expires_in,
                "created_at": current_time,
                "token_type": "Bearer"
            }

            cache.set("tokens_siaf", tokens, timeout)
            
        except Exception as e:
            print(f"Error al guardar los tokens: {e}")
            return e
        
    def get_access_token(self):
        try:

            # return "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJBeGxPdUtBVjBMN0xCa2k5VHhTcmxCaE92QUZzdzNCQjF3RWRfQmlXaGdJIn0.eyJleHAiOjE3NTE1NjI0NzgsImlhdCI6MTc1MTU1ODg3OCwiYXV0aF90aW1lIjoxNzUxNTU4ODc2LCJqdGkiOiI4ZGFmMTgyNi0xNDliLTQ5MzUtOWE1MS03NTFkZmY1MjEwNWMiLCJpc3MiOiJodHRwczovL2F1dGhvcml6ZS5tZWYuZ29iLnBlL2F1dGgvcmVhbG1zL21lZiIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiJmOjM2MGVjNWEwLTBlMjctNDM2OS04NzgxLTAwYzg4ZjMzMzc1MzowMjg5NzA0MSIsInR5cCI6IkJlYXJlciIsImF6cCI6Imp3dENsaWVudCIsInNlc3Npb25fc3RhdGUiOiI5NmZmNWUzMi1hODIxLTQ5OTQtYmE5Ni1lMzlhZmI4YjNkN2EiLCJhY3IiOiIxIiwiYWxsb3dlZC1vcmlnaW5zIjpbIioiXSwicmVhbG1fYWNjZXNzIjp7InJvbGVzIjpbIm9mZmxpbmVfYWNjZXNzIiwidW1hX2F1dGhvcml6YXRpb24iXX0sInJlc291cmNlX2FjY2VzcyI6eyJhY2NvdW50Ijp7InJvbGVzIjpbIm1hbmFnZS1hY2NvdW50IiwibWFuYWdlLWFjY291bnQtbGlua3MiLCJ2aWV3LXByb2ZpbGUiXX19LCJzY29wZSI6ImVtYWlsIHJlYWQgd3JpdGUgcHJvZmlsZSIsInNpZCI6Ijk2ZmY1ZTMyLWE4MjEtNDk5NC1iYTk2LWUzOWFmYjhiM2Q3YSIsImVtYWlsX3ZlcmlmaWVkIjpmYWxzZSwiYXBlbGxpZG9wYXRlcm5vIjoiTUVESU5BIiwicHJlZmVycmVkX3VzZXJuYW1lIjoiMDI4OTcwNDEiLCJnaXZlbl9uYW1lIjoiTUFSSU8gQUxFWEFOREVSIiwibm9tYnJlIjoiTUFSSU8gQUxFWEFOREVSIiwibm9tYnJldXN1YXJpbyI6Ik1BUklPIEFMRVhBTkRFUiBNRURJTkEgTUFSUVVFWiIsInVuaWRhZGVqZWN1dG9yYSI6IjMwMTUyOSIsImVudGlkYWQiOiJNVU5JQ0lQQUxJREFEIFBST1ZJTkNJQUwgREUgUElVUkEiLCJhcGVsbGlkb21hdGVybm8iOiJNQVJRVUVaIiwibmFtZSI6Ik1BUklPIEFMRVhBTkRFUiBNRURJTkEgTUFSUVVFWiIsImZhbWlseV9uYW1lIjoiTUVESU5BIE1BUlFVRVoiLCJ0aXBvdW5pZGFkIjoiTSIsInVzZXJuYW1lIjoiMDI4OTcwNDEifQ.PF8YMu4d_961ZscBzz21dKcqUMi1Fldzwyo58TI7J-WAMTpL0a6ctHtSLSI4r7OkquedtPMRK8mb-RlTHKMUt8tVi8R8L_P7PluRvKTc0Z5Ty8CnHSIGUdkPNpaqTzDQMFYneh8v81BWpNeutVPyTgt-P6nFQyYilAcGQPvSkspoH8P1417wTyDGybVYE03AE2tqsq2CJE0Mua_ZawWd6QRGJkoJXj1FG2BHBMNWeqr2UScCDYsaYzBXZt6dI7YzzHu2uEJrbY6WVFMZcuWa4XAnbVa8hFRrSaYAJbAwwLEZO_j58lCOL-TTySxTAnF0QFVGrQV0rHWIaSIpbpIAZw"

            # Verificar si ya hay un lock
            if self.is_lock_active():                
                return cache.get("tokens_siaf", None).get("access_token", None)
                       
            
            if not self.refresh_token_is_valid():                
                self.acquire_get_tokens_lock()
                access_token, refresh_token = self.login_siaf(os.environ.get('SIAFWEB_USERNAME'), os.environ.get('SIAFWEB_PASSWORD'))
                self.save_tokens(access_token, refresh_token)              
                self.release_get_tokens_lock()
            else:                
                if self.is_necesary_renew_tokens():                 
                    self.acquire_get_tokens_lock()
                    tokens = cache.get("tokens_siaf", None)
                    refresh_token = tokens.get("refresh_token", None)
                    client_secret = "aa0c08b2-87d9-466e-88fc-26c2e8170c9d"
                    access_token, refresh_token = self.renew_tokens(refresh_token, client_secret)
                    self.save_tokens(access_token, refresh_token)
                    self.release_get_tokens_lock()
                                      
            return cache.get("tokens_siaf", None).get("access_token", None)
            

        except Exception as e:
            self.release_get_tokens_lock()
            print(f"Error al obtener los tokens: {e}")
            return e
        
        

    def refresh_token_is_valid(self):
        try:
            tokens = cache.get("tokens_siaf", None)
            if not tokens:
                return False
            
            if tokens.get("refresh_token_expires_at", 0) < time.time():
                return False
            
            return True
        except Exception as e:
            print(f"Error al verificar si el token de refresh es válido: {e}")
            return e
        
    def renew_tokens(self, refresh_token, client_secret):
        try:

            url_refresh = "https://authorize.mef.gob.pe/auth/realms/mef/protocol/openid-connect/token"

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
               
            }

            data = {
                "grant_type": "refresh_token",
                "client_id": "jwtClient",
                "refresh_token": refresh_token,
                "client_secret": client_secret
            }

            response = requests.post(url_refresh, headers=headers, data=data)

            response_json = response.json()

            access_token = response_json.get("access_token", None)
            refresh_token = response_json.get("refresh_token", None)

            return access_token, refresh_token
        except Exception as e:
            print(f"Error al actualizar el token de refresh: {e}")
            return e
        

    def is_necesary_renew_tokens(self):
        try:
            tokens = cache.get("tokens_siaf", None)
            if not tokens:
                return False
            
            
            if tokens.get("refresh_token_expires_at", 0) < time.time() + TOKEN_REFRESH_THRESHOLD:
                return True
            
            return False
            
        except Exception as e:
            print(f"Error al verificar si es necesario actualizar los tokens: {e}")
            return e
        
        