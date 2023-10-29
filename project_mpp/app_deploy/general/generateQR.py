
import urllib.parse

def generateQrURL(data, dimensions="300x300"):
    # Codificar los datos en formato URL
    encoded_data = urllib.parse.quote(data)
    
    # Construir la URL de la API de Google Chart
    url = f"https://chart.googleapis.com/chart?cht=qr&chs={dimensions}&chl={encoded_data}"
    
    # Devolver la URL generada
    return url