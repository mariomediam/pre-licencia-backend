from django.core.files.storage import FileSystemStorage
from dotenv import load_dotenv

def upload_file(file, location, file_name):
    # max_length => indica el maximo de caracteres en el nombre de un archivo
    # use_url => si es True, el valor de la url sera usado para mostrar la ubicacion del archivo. si es False entonces se usara el nombre del archivo  (False es su valor x defecto)
    archivo = InMemoryUploadedFile = file
        
    # para ver el tipo de archivo que es
    # print(archivo.content_type)
    # para ver el nombre del archivo
    # print(archivo.name)
    # para ver el tamaño del archivo  expresado en bytes
    # print(archivo.size)

    # NOTA: una vez que se usa el metodo read() se elimina la informacion de ese archivo en la memoria RAM

    fs = FileSystemStorage(location=location)
    file = fs.save(file_name, archivo)            
    
    return True

