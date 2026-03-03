# Excel Utils - Utilidades de Exportación

Este módulo proporciona funciones reutilizables para exportar datos JSON a archivos Excel con formato profesional.

## Ubicación

`app_deploy/general/excel_utils.py`

## Funciones Disponibles

### 1. `create_excel_from_json(data, sheet_name="Datos", headers=None)`

Crea un archivo Excel con una sola hoja a partir de datos JSON.

#### Parámetros

- **data** (list): Lista de diccionarios con los datos a exportar
- **sheet_name** (str, opcional): Nombre de la hoja. Default: "Datos"
- **headers** (list, opcional): Lista de headers personalizados. Si no se proporciona, usa las keys del primer elemento

#### Retorna

- **io.BytesIO**: Buffer con el archivo Excel generado

#### Ejemplo de Uso

```python
from app_deploy.general.excel_utils import create_excel_from_json
from django.http import HttpResponse

def exportar_usuarios(request):
    # Obtener datos de la base de datos o cualquier fuente
    usuarios = [
        {"nombre": "Juan Pérez", "edad": 30, "ciudad": "Lima"},
        {"nombre": "María García", "edad": 25, "ciudad": "Arequipa"},
        {"nombre": "Pedro López", "edad": 35, "ciudad": "Cusco"}
    ]
    
    # Crear el Excel
    output = create_excel_from_json(
        data=usuarios,
        sheet_name="Usuarios",
        headers=["Nombre Completo", "Edad", "Ciudad de Residencia"]
    )
    
    # Retornar como respuesta HTTP
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="usuarios.xlsx"'
    
    return response
```

---

### 2. `create_excel_with_multiple_sheets(sheets_data)`

Crea un archivo Excel con múltiples hojas a partir de datos JSON.

#### Parámetros

- **sheets_data** (list): Lista de diccionarios con la configuración de cada hoja. Cada diccionario debe tener:
  - `sheet_name` (str): Nombre de la hoja
  - `data` (list): Lista de diccionarios con los datos
  - `headers` (list, opcional): Headers personalizados

#### Retorna

- **io.BytesIO**: Buffer con el archivo Excel generado

#### Ejemplo de Uso

```python
from app_deploy.general.excel_utils import create_excel_with_multiple_sheets
from django.http import HttpResponse

def exportar_reporte_completo(request):
    # Preparar datos para múltiples hojas
    sheets = [
        {
            'sheet_name': 'Usuarios',
            'data': [
                {"nombre": "Juan", "email": "juan@example.com", "rol": "Admin"},
                {"nombre": "María", "email": "maria@example.com", "rol": "Usuario"}
            ],
            'headers': ['Nombre', 'Correo Electrónico', 'Rol']
        },
        {
            'sheet_name': 'Productos',
            'data': [
                {"producto": "Laptop", "precio": 1200, "stock": 15},
                {"producto": "Mouse", "precio": 25, "stock": 50}
            ]
        },
        {
            'sheet_name': 'Ventas',
            'data': [
                {"fecha": "2024-01-15", "cliente": "Empresa A", "monto": 5000},
                {"fecha": "2024-01-16", "cliente": "Empresa B", "monto": 3500}
            ]
        }
    ]
    
    # Crear el Excel con múltiples hojas
    output = create_excel_with_multiple_sheets(sheets)
    
    # Retornar como respuesta HTTP
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="reporte_completo.xlsx"'
    
    return response
```

---

## Características del Excel Generado

### Estilos Aplicados

- **Headers:**
  - Fondo azul (#4472C4)
  - Texto blanco en negrita (tamaño 11)
  - Centrado horizontal y vertical
  - Bordes delgados

- **Celdas de Datos:**
  - Bordes delgados en todas las celdas
  - Ancho de columna ajustado automáticamente (máximo 50 caracteres)

### Formato Automático

- **Fechas:** Las fechas en formato ISO (con 'T' o '-') se formatean automáticamente a `dd/mm/yyyy HH:MM:SS`

---

## Casos de Uso Comunes

### Caso 1: Exportar Resultados de una Consulta

```python
from app_deploy.general.excel_utils import create_excel_from_json
from .models import MiModelo

def exportar_datos(request):
    # Obtener datos del modelo
    datos = MiModelo.objects.filter(activo=True).values(
        'nombre', 'descripcion', 'fecha_creacion'
    )
    
    # Convertir QuerySet a lista
    datos_list = list(datos)
    
    # Crear Excel
    output = create_excel_from_json(
        data=datos_list,
        sheet_name="Datos Activos"
    )
    
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="datos_activos.xlsx"'
    return response
```

### Caso 2: Exportar con Headers en Español

```python
from app_deploy.general.excel_utils import create_excel_from_json

def exportar_vehiculos(request):
    # Datos con keys en inglés
    vehiculos = [
        {"plate": "ABC-123", "brand": "Toyota", "model": "Corolla", "year": 2020},
        {"plate": "DEF-456", "brand": "Honda", "model": "Civic", "year": 2019}
    ]
    
    # Crear Excel con headers en español
    output = create_excel_from_json(
        data=vehiculos,
        sheet_name="Vehículos",
        headers=["Placa", "Marca", "Modelo", "Año"]
    )
    
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="vehiculos.xlsx"'
    return response
```

### Caso 3: Exportar Datos Vacíos con Headers

```python
from app_deploy.general.excel_utils import create_excel_from_json

def exportar_plantilla(request):
    # Crear Excel vacío con solo headers
    output = create_excel_from_json(
        data=[],  # Sin datos
        sheet_name="Plantilla",
        headers=["Nombre", "Apellido", "Email", "Teléfono"]
    )
    
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="plantilla_usuarios.xlsx"'
    return response
```

### Caso 4: Reporte Mensual con Múltiples Hojas

```python
from app_deploy.general.excel_utils import create_excel_with_multiple_sheets
from .models import Venta, Cliente, Producto

def exportar_reporte_mensual(request, anio, mes):
    # Obtener datos de diferentes modelos
    ventas = list(Venta.objects.filter(
        fecha__year=anio, 
        fecha__month=mes
    ).values('fecha', 'cliente__nombre', 'monto'))
    
    clientes = list(Cliente.objects.filter(
        activo=True
    ).values('nombre', 'email', 'telefono'))
    
    productos = list(Producto.objects.all().values(
        'nombre', 'precio', 'stock'
    ))
    
    # Preparar hojas
    sheets = [
        {
            'sheet_name': f'Ventas {mes}/{anio}',
            'data': ventas,
            'headers': ['Fecha', 'Cliente', 'Monto (S/)']
        },
        {
            'sheet_name': 'Clientes Activos',
            'data': clientes,
            'headers': ['Nombre', 'Email', 'Teléfono']
        },
        {
            'sheet_name': 'Inventario',
            'data': productos,
            'headers': ['Producto', 'Precio', 'Stock']
        }
    ]
    
    # Crear Excel
    output = create_excel_with_multiple_sheets(sheets)
    
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = f'attachment; filename="reporte_{mes}_{anio}.xlsx"'
    return response
```

---

## Integración con Serializers

Si usas Django REST Framework, puedes combinar estas utilidades con serializers:

```python
from rest_framework import serializers
from app_deploy.general.excel_utils import create_excel_from_json
from .models import Usuario
from .serializers import UsuarioSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def exportar_usuarios_excel(request):
    # Obtener usuarios
    usuarios = Usuario.objects.all()
    
    # Serializar datos
    serializer = UsuarioSerializer(usuarios, many=True)
    
    # Crear Excel
    output = create_excel_from_json(
        data=serializer.data,
        sheet_name="Usuarios"
    )
    
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="usuarios.xlsx"'
    return response
```

---

## Manejo de Errores

```python
from app_deploy.general.excel_utils import create_excel_from_json
from rest_framework.response import Response
from rest_framework import status

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def exportar_datos_custom(request):
    try:
        datos = request.data.get('datos')
        
        if not datos:
            return Response(
                {"message": "No se proporcionaron datos"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not isinstance(datos, list):
            return Response(
                {"message": "Los datos deben ser un array"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Crear Excel
        output = create_excel_from_json(datos, "Datos")
        
        response = HttpResponse(
            output.getvalue(), 
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = 'attachment; filename="export.xlsx"'
        return response
        
    except Exception as e:
        return Response(
            {"message": f"Error al generar Excel: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
```

---

## Dependencias

- **openpyxl**: Librería para crear archivos Excel (ya instalada en el proyecto)

---

## Notas Importantes

1. **Tamaño de Datos:** Para grandes volúmenes de datos (>10,000 registros), considera implementar paginación o procesamiento en segundo plano.

2. **Memoria:** Los archivos Excel se generan en memoria (BytesIO). Para archivos muy grandes, considera escribir directamente a disco.

3. **Formato de Fechas:** Las fechas se formatean automáticamente. Si necesitas un formato diferente, modifica el código en `excel_utils.py`.

4. **Ancho de Columnas:** El ancho máximo de columna está limitado a 50 caracteres. Ajusta este valor según tus necesidades.

---

## Soporte

Para más información o mejoras, contacta al equipo de desarrollo.
