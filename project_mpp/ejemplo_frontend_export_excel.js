/**
 * EJEMPLO DE USO DEL ENDPOINT DE EXPORTACIÓN A EXCEL
 * 
 * Endpoints disponibles:
 * - POST /api/export-json-to-excel/ (una hoja)
 * - POST /api/export-json-to-excel-multiple/ (múltiples hojas)
 * 
 * Ubicación: app_deploy - Puede ser usado desde cualquier app del proyecto
 * 
 * Este archivo muestra cómo enviar un JSON desde el frontend y recibir un archivo Excel
 */

// ============================================
// EJEMPLO 1: Exportación básica con fetch
// ============================================
async function exportarJsonAExcelBasico(datos) {
    try {
        const response = await fetch('/api/export-json-to-excel/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}` // O tu método de autenticación
            },
            body: JSON.stringify({
                data: datos,
                filename: 'mi_reporte.xlsx',
                sheet_name: 'Reporte'
            })
        });

        if (!response.ok) {
            throw new Error('Error al generar el Excel');
        }

        // Convertir la respuesta a blob
        const blob = await response.blob();
        
        // Crear un enlace temporal para descargar el archivo
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'mi_reporte.xlsx';
        document.body.appendChild(a);
        a.click();
        
        // Limpiar
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        console.log('Excel descargado exitosamente');
    } catch (error) {
        console.error('Error al exportar:', error);
        alert('Error al generar el archivo Excel');
    }
}

// ============================================
// EJEMPLO 2: Con axios (más común en React/Vue)
// ============================================
async function exportarJsonAExcelConAxios(datos) {
    try {
        const response = await axios.post('/api/export-json-to-excel/', {
            data: datos,
            filename: 'mi_reporte.xlsx',
            sheet_name: 'Reporte'
        }, {
            responseType: 'blob', // Importante para recibir el archivo
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            }
        });

        // Crear el enlace de descarga
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'mi_reporte.xlsx');
        document.body.appendChild(link);
        link.click();
        link.remove();
        
        console.log('Excel descargado exitosamente');
    } catch (error) {
        console.error('Error al exportar:', error);
        alert('Error al generar el archivo Excel');
    }
}

// ============================================
// EJEMPLO 3: Con headers personalizados
// ============================================
async function exportarConHeadersPersonalizados(datos) {
    try {
        const response = await fetch('/api/export-json-to-excel/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                data: datos,
                filename: 'reporte_personalizado.xlsx',
                sheet_name: 'Datos Personalizados',
                headers: ['Nombre', 'Apellido', 'Email', 'Teléfono'] // Headers en español
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al generar el Excel');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'reporte_personalizado.xlsx';
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
    } catch (error) {
        console.error('Error:', error);
        alert(error.message);
    }
}

// ============================================
// EJEMPLO 4: Función reutilizable completa
// ============================================
/**
 * Función genérica para exportar cualquier JSON a Excel
 * @param {Array} data - Array de objetos JSON
 * @param {Object} options - Opciones de configuración
 * @param {string} options.filename - Nombre del archivo (opcional)
 * @param {string} options.sheetName - Nombre de la hoja (opcional)
 * @param {Array} options.headers - Headers personalizados (opcional)
 * @param {string} options.apiUrl - URL del API (opcional)
 * @returns {Promise<void>}
 */
async function exportarJsonAExcel(data, options = {}) {
    const {
        filename = 'export.xlsx',
        sheetName = 'Datos',
        headers = null,
        apiUrl = '/api/export-json-to-excel/'
    } = options;

    try {
        // Validar que haya datos
        if (!data || !Array.isArray(data) || data.length === 0) {
            throw new Error('No hay datos para exportar');
        }

        // Realizar la petición
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                data: data,
                filename: filename,
                sheet_name: sheetName,
                headers: headers
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al generar el Excel');
        }

        // Descargar el archivo
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        
        // Limpiar
        setTimeout(() => {
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }, 100);

        return { success: true, message: 'Excel descargado exitosamente' };
    } catch (error) {
        console.error('Error al exportar a Excel:', error);
        return { success: false, message: error.message };
    }
}

// ============================================
// EJEMPLOS DE USO
// ============================================

// Ejemplo 1: Datos simples
const datosSimples = [
    { nombre: 'Juan', edad: 30, ciudad: 'Lima' },
    { nombre: 'María', edad: 25, ciudad: 'Arequipa' },
    { nombre: 'Pedro', edad: 35, ciudad: 'Cusco' }
];

// Uso básico
// exportarJsonAExcel(datosSimples);

// Ejemplo 2: Con opciones personalizadas
// exportarJsonAExcel(datosSimples, {
//     filename: 'usuarios.xlsx',
//     sheetName: 'Lista de Usuarios',
//     headers: ['Nombre Completo', 'Edad', 'Ciudad de Residencia']
// });

// Ejemplo 3: Datos de una tabla HTML
function exportarTablaAExcel() {
    // Obtener datos de una tabla
    const tabla = document.querySelector('#miTabla');
    const filas = tabla.querySelectorAll('tbody tr');
    
    const datos = Array.from(filas).map(fila => {
        const celdas = fila.querySelectorAll('td');
        return {
            columna1: celdas[0].textContent,
            columna2: celdas[1].textContent,
            columna3: celdas[2].textContent
        };
    });
    
    exportarJsonAExcel(datos, {
        filename: 'tabla_exportada.xlsx',
        sheetName: 'Datos de Tabla'
    });
}

// Ejemplo 4: Datos de una API
async function exportarDatosDeAPI() {
    try {
        // Obtener datos de tu API
        const response = await fetch('/api/transporte/vehiculos-vigentes/');
        const result = await response.json();
        
        // Exportar los datos
        await exportarJsonAExcel(result.content, {
            filename: 'vehiculos_vigentes.xlsx',
            sheetName: 'Vehículos'
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

// Ejemplo 5: React Component
/*
import React, { useState } from 'react';

function ExportButton({ datos }) {
    const [loading, setLoading] = useState(false);

    const handleExport = async () => {
        setLoading(true);
        try {
            const result = await exportarJsonAExcel(datos, {
                filename: 'reporte.xlsx',
                sheetName: 'Datos'
            });
            
            if (result.success) {
                alert('Excel descargado exitosamente');
            } else {
                alert('Error: ' + result.message);
            }
        } catch (error) {
            alert('Error al exportar');
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
*/

// Ejemplo 6: Vue Component
/*
<template>
  <button @click="exportar" :disabled="loading">
    {{ loading ? 'Exportando...' : 'Exportar a Excel' }}
  </button>
</template>

<script>
export default {
  data() {
    return {
      loading: false
    }
  },
  methods: {
    async exportar() {
      this.loading = true;
      try {
        await exportarJsonAExcel(this.datos, {
          filename: 'reporte.xlsx',
          sheetName: 'Datos'
        });
        this.$message.success('Excel descargado exitosamente');
      } catch (error) {
        this.$message.error('Error al exportar');
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>
*/

// ============================================
// EJEMPLO 7: Exportar múltiples hojas en un solo archivo
// ============================================
async function exportarMultiplesHojas(sheetsData, filename = 'reporte_completo.xlsx') {
    try {
        const response = await fetch('/api/export-json-to-excel-multiple/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('token')}`
            },
            body: JSON.stringify({
                sheets: sheetsData,
                filename: filename
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Error al generar el Excel');
        }

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        
        setTimeout(() => {
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        }, 100);

        return { success: true, message: 'Excel con múltiples hojas descargado exitosamente' };
    } catch (error) {
        console.error('Error al exportar múltiples hojas:', error);
        return { success: false, message: error.message };
    }
}

// Ejemplo de uso de múltiples hojas
/*
const sheetsData = [
    {
        sheet_name: 'Usuarios',
        data: [
            { nombre: 'Juan', email: 'juan@example.com', rol: 'Admin' },
            { nombre: 'María', email: 'maria@example.com', rol: 'Usuario' }
        ],
        headers: ['Nombre Completo', 'Correo Electrónico', 'Rol']
    },
    {
        sheet_name: 'Productos',
        data: [
            { producto: 'Laptop', precio: 1200, stock: 15 },
            { producto: 'Mouse', precio: 25, stock: 50 }
        ]
    },
    {
        sheet_name: 'Ventas',
        data: [
            { fecha: '2024-01-15', cliente: 'Empresa A', monto: 5000 },
            { fecha: '2024-01-16', cliente: 'Empresa B', monto: 3500 }
        ],
        headers: ['Fecha', 'Cliente', 'Monto (S/)']
    }
];

exportarMultiplesHojas(sheetsData, 'reporte_mensual.xlsx');
*/

// ============================================
// EXPORTAR PARA USO EN MÓDULOS
// ============================================
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { 
        exportarJsonAExcel,
        exportarMultiplesHojas
    };
}
