import os
import base64

def imageToBase64(ruta_imagen):
    # Convirtiendo imagen a base64            
    imagen_codificada = None

    if os.path.exists(ruta_imagen.strip()):            
        with open(ruta_imagen, "rb") as f:
            imagen_codificada = base64.b64encode(f.read()).decode("utf-8")
    
    return imagen_codificada
