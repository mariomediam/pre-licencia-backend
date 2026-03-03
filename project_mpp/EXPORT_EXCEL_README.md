# Exportación de JSON a Excel - Documentación

## Descripción General

Este sistema permite exportar cualquier JSON desde el frontend al backend y recibir un archivo Excel formateado automáticamente.

**Ubicación:** Los endpoints están en `app_deploy` para que puedan ser utilizados desde cualquier app del proyecto.

## Características

✅ Exportación genérica de cualquier JSON a Excel  
✅ Headers personalizables  
✅ Nombre de archivo y hoja personalizables  
✅ Formato automático de fechas  
✅ Estilos profesionales (bordes, colores, alineación)  
✅ Ajuste automático del ancho de columnas  
✅ Manejo de errores robusto  
✅ Soporte para múltiples hojas en un solo archivo  

---

## Backend (Django)

### Endpoint Principal - Una Hoja

**URL:** `POST /api/export-json-to-excel/`  
**Autenticación:** Requerida (Token Bearer)  
**Content-Type:** `application/json`

### Endpoint Avanzado - Múltiples Hojas

**URL:** `POST /api/export-json-to-excel-multiple/`  
**Autenticación:** Requerida (Token Bearer)  
**Content-Type:** `application/json`

### Request Body

```json
{
  "data": [
    { "campo1": "valor1", "campo2": "valor2" },
    { "campo1": "valor3", "campo2": "valor4" }
  ],
  "filename": "mi_archivo.xlsx",
  "sheet_name": "Hoja1",
  "headers": ["Columna 1", "Columna 2"]
}
```

### Parámetros

| Parámetro | Tipo | Requerido | Descripción | Default |
|-----------|------|-----------|-------------|---------|
| `data` | Array | ✅ Sí | Array de objetos JSON con los datos a exportar | - |
| `filename` | String | ❌ No | Nombre del archivo Excel (se agrega .xlsx automáticamente) | `export.xlsx` |
| `sheet_name` | String | ❌ No | Nombre de la hoja en el Excel | `Datos` |
| `headers` | Array | ❌ No | Headers personalizados. Si no se proporciona, usa las keys del primer objeto | Keys del JSON |

### Respuesta Exitosa

**Status Code:** `200 OK`  
**Content-Type:** `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`  
**Headers:** `Content-Disposition: attachment; filename="archivo.xlsx"`

El archivo Excel se descarga automáticamente.

### Respuestas de Error

#### 400 Bad Request - Falta el parámetro data
```json
{
  "message": "El parámetro 'data' es requerido",
  "content": null
}
```

#### 400 Bad Request - Data no es un array
```json
{
  "message": "El parámetro 'data' debe ser un array",
  "content": null
}
```

#### 500 Internal Server Error
```json
{
  "message": "Error al generar el Excel: [detalle del error]",
  "content": null
}
```

---

## Endpoint de Múltiples Hojas

### Request Body para Múltiples Hojas

```json
{
  "sheets": [
    {
      "sheet_name": "Usuarios",
      "data": [
        { "nombre": "Juan", "edad": 30 },
        { "nombre": "María", "edad": 25 }
      ],
      "headers": ["Nombre Completo", "Edad"]
    },
    {
      "sheet_name": "Productos",
      "data": [
        { "producto": "Laptop", "precio": 1200 },
        { "producto": "Mouse", "precio": 25 }
      ]
    }
  ],
  "filename": "reporte_completo.xlsx"
}
```

### Ejemplo de Uso - Múltiples Hojas

```javascript
async function exportarMultiplesHojas() {
    const response = await fetch('/api/export-json-to-excel-multiple/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            sheets: [
                {
                    sheet_name: 'Usuarios',
                    data: datosUsuarios,
                    headers: ['Nombre', 'Email', 'Rol']
                },
                {
                    sheet_name: 'Productos',
                    data: datosProductos
                }
            ],
            filename: 'reporte_completo.xlsx'
        })
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'reporte_completo.xlsx';
    a.click();
    window.URL.revokeObjectURL(url);
}
```

---

## Frontend

### Opción 1: Fetch API (JavaScript Vanilla)

```javascript
async function exportarAExcel(datos) {
    const response = await fetch('/api/export-json-to-excel/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
            data: datos,
            filename: 'reporte.xlsx',
            sheet_name: 'Reporte'
        })
    });

    const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'reporte.xlsx';
    a.click();
    window.URL.revokeObjectURL(url);
}
```

### Opción 2: Axios (React/Vue)

```javascript
import axios from 'axios';

async function exportarAExcel(datos) {
    const response = await axios.post('/api/export-json-to-excel/', {
        data: datos,
        filename: 'reporte.xlsx',
        sheet_name: 'Reporte'
    }, {
        responseType: 'blob', // ¡Importante!
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });

    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', 'reporte.xlsx');
    document.body.appendChild(link);
    link.click();
    link.remove();
}
```

### Opción 3: React Component Completo

```jsx
import React, { useState } from 'react';
import axios from 'axios';

function ExportButton({ datos, filename = 'export.xlsx' }) {
    const [loading, setLoading] = useState(false);

    const handleExport = async () => {
        setLoading(true);
        try {
            const response = await axios.post(
                '/api/transporte/export-json-to-excel/',
                {
                    data: datos,
                    filename: filename,
                    sheet_name: 'Datos'
                },
                {
                    responseType: 'blob',
                    headers: {
                        'Authorization': `Bearer ${localStorage.getItem('token')}`
                    }
                }
            );

            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            
            alert('Excel descargado exitosamente');
        } catch (error) {
            console.error('Error:', error);
            alert('Error al exportar el archivo');
        } finally {
            setLoading(false);
        }
    };

    return (
        <button onClick={handleExport} disabled={loading}>
            {loading ? 'Exportando...' : 'Exportar a Excel'}
        </button>
    );
}

export default ExportButton;
```

### Opción 4: Vue Component

```vue
<template>
  <button @click="exportar" :disabled="loading">
    {{ loading ? 'Exportando...' : 'Exportar a Excel' }}
  </button>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    datos: {
      type: Array,
      required: true
    },
    filename: {
      type: String,
      default: 'export.xlsx'
    }
  },
  data() {
    return {
      loading: false
    }
  },
  methods: {
    async exportar() {
      this.loading = true;
      try {
        const response = await axios.post(
          '/api/transporte/export-json-to-excel/',
          {
            data: this.datos,
            filename: this.filename,
            sheet_name: 'Datos'
          },
          {
            responseType: 'blob',
            headers: {
              'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
          }
        );

        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.filename);
        document.body.appendChild(link);
        link.click();
        link.remove();
        
        this.$message.success('Excel descargado exitosamente');
      } catch (error) {
        console.error('Error:', error);
        this.$message.error('Error al exportar el archivo');
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
```

---

## Ejemplos de Uso

### Ejemplo 1: Datos Simples

```javascript
const datos = [
    { nombre: 'Juan Pérez', edad: 30, ciudad: 'Lima' },
    { nombre: 'María García', edad: 25, ciudad: 'Arequipa' },
    { nombre: 'Pedro López', edad: 35, ciudad: 'Cusco' }
];

// Exportar con configuración por defecto
exportarAExcel(datos);
```

### Ejemplo 2: Con Headers Personalizados

```javascript
const datos = [
    { name: 'John', age: 30, city: 'Lima' },
    { name: 'Mary', age: 25, city: 'Arequipa' }
];

// Los datos tienen keys en inglés, pero queremos headers en español
await fetch('/api/transporte/export-json-to-excel/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify({
        data: datos,
        filename: 'usuarios.xlsx',
        sheet_name: 'Usuarios',
        headers: ['Nombre', 'Edad', 'Ciudad'] // Headers personalizados
    })
});
```

### Ejemplo 3: Exportar Datos de una Tabla

```javascript
function exportarTabla() {
    const tabla = document.querySelector('#miTabla');
    const filas = tabla.querySelectorAll('tbody tr');
    
    const datos = Array.from(filas).map(fila => {
        const celdas = fila.querySelectorAll('td');
        return {
            columna1: celdas[0].textContent.trim(),
            columna2: celdas[1].textContent.trim(),
            columna3: celdas[2].textContent.trim()
        };
    });
    
    exportarAExcel(datos);
}
```

### Ejemplo 4: Exportar Resultado de una API

```javascript
async function exportarVehiculosVigentes() {
    try {
        // 1. Obtener datos de la API
        const response = await fetch('/api/transporte/vehiculos-vigentes/', {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        const result = await response.json();
        
        // 2. Exportar a Excel
        const exportResponse = await fetch('/api/transporte/export-json-to-excel/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                data: result.content,
                filename: 'vehiculos_vigentes.xlsx',
                sheet_name: 'Vehículos'
            })
        });
        
        // 3. Descargar el archivo
        const blob = await exportResponse.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'vehiculos_vigentes.xlsx';
        a.click();
        window.URL.revokeObjectURL(url);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Error al exportar');
    }
}
```

---

## Formato del Excel Generado

El archivo Excel generado incluye:

- **Headers con estilo:**
  - Fondo azul (#4472C4)
  - Texto blanco en negrita
  - Centrado horizontal y vertical
  - Bordes delgados

- **Datos:**
  - Bordes delgados en todas las celdas
  - Ancho de columna ajustado automáticamente
  - Fechas formateadas (dd/mm/yyyy HH:MM:SS)

- **Características:**
  - Máximo ancho de columna: 50 caracteres
  - Formato: `.xlsx` (Excel 2007+)

---

## Notas Importantes

1. **Autenticación:** El endpoint requiere autenticación. Asegúrate de incluir el token en el header `Authorization`.

2. **Tamaño de datos:** Para grandes volúmenes de datos (>10,000 registros), considera implementar paginación o procesamiento en segundo plano.

3. **Formato de fechas:** Las fechas en formato ISO (con 'T' o '-') se formatean automáticamente a dd/mm/yyyy HH:MM:SS.

4. **Headers personalizados:** Si proporcionas headers personalizados, deben coincidir con el orden de las keys en los objetos del array `data`.

5. **Extensión del archivo:** Si no incluyes `.xlsx` en el filename, se agregará automáticamente.

6. **CORS:** Si el frontend está en un dominio diferente, asegúrate de configurar CORS correctamente en Django.

---

## Solución de Problemas

### El archivo no se descarga

**Problema:** La petición se completa pero el archivo no se descarga.

**Solución:** Verifica que estés usando `responseType: 'blob'` en axios o convirtiendo la respuesta a blob con fetch.

```javascript
// Con fetch
const blob = await response.blob();

// Con axios
{ responseType: 'blob' }
```

### Error 401 Unauthorized

**Problema:** El backend rechaza la petición.

**Solución:** Verifica que el token de autenticación sea válido y esté incluido correctamente:

```javascript
headers: {
    'Authorization': `Bearer ${token}` // Nota el espacio después de "Bearer"
}
```

### Error 400 Bad Request

**Problema:** El parámetro `data` no es válido.

**Solución:** Asegúrate de que:
- `data` sea un array
- `data` contenga objetos (no strings o números)
- El JSON esté bien formado

```javascript
// ✅ Correcto
{ data: [{ nombre: 'Juan' }] }

// ❌ Incorrecto
{ data: { nombre: 'Juan' } }  // No es un array
{ data: ['Juan', 'María'] }    // Array de strings, no objetos
```

### El Excel está vacío

**Problema:** El archivo se descarga pero no tiene datos.

**Solución:** Verifica que el array `data` no esté vacío y que los objetos tengan propiedades.

---

## Dependencias

### Backend (Python)
- `openpyxl` - Ya está instalado en tu proyecto

### Frontend
- Ninguna librería especial requerida
- Opcionalmente: `axios` para peticiones HTTP más sencillas

---

## Código Fuente

### Backend
- **Utilidades Excel:** `app_deploy/general/excel_utils.py`
  - `create_excel_from_json()` - Función para crear Excel con una hoja
  - `create_excel_with_multiple_sheets()` - Función para crear Excel con múltiples hojas
  
- **Views:** `app_deploy/views.py`
  - `ExportJsonToExcelController()` - Endpoint para una hoja
  - `ExportJsonToExcelMultipleSheetsController()` - Endpoint para múltiples hojas
  
- **URLs:** `app_deploy/urls.py`
  - `/api/export-json-to-excel/` - Ruta para una hoja
  - `/api/export-json-to-excel-multiple/` - Ruta para múltiples hojas

### Frontend
- **Ejemplos:** `ejemplo_frontend_export_excel.js`
- **Página de Prueba:** `test_export_excel.html`

### Uso desde otras apps

Para usar estas utilidades desde otras apps (como `app_transporte`), simplemente importa las funciones:

```python
from app_deploy.general.excel_utils import create_excel_from_json

# En tu view
def mi_export_view(request):
    datos = [{"nombre": "Juan", "edad": 30}]
    output = create_excel_from_json(datos, "MiHoja")
    
    response = HttpResponse(
        output.getvalue(), 
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response['Content-Disposition'] = 'attachment; filename="mi_archivo.xlsx"'
    return response
```

---

## Soporte

Para más información o problemas, contacta al equipo de desarrollo.
