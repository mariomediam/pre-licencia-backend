from django.urls import reverse
import urllib.parse

# def generateQrURL(data, dimensions="300x300"):
#     # Codificar los datos en formato URL
#     encoded_data = urllib.parse.quote(data)
    
#     # Construir la URL de la API de Google Chart
#     url = f"https://chart.googleapis.com/chart?cht=qr&chs={dimensions}&chl={encoded_data}"
    
#     # Devolver la URL generada
#     return url

def generateQrURL(data, scale=5, border=1):
    # Codificar los datos en formato URL
    if data.startswith('http'):
        encoded_data = data.replace('&', '%26')
    else:
        encoded_data = data


    # Genera la URL relativa
    url = "http://192.168.100.59:8000"
    url += reverse('generate_qr')    
    url += f"?scale{scale}&border={border}&data={encoded_data}"
    
    # Devolver la URL generada
    return url