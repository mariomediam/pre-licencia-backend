from celery import shared_task
from celery.utils.log import get_task_logger
from datetime import datetime
from app_indicadores.indicadores import S42SincronizaRecaudacion

logger = get_task_logger(__name__)

@shared_task
def sincroniza_recaudacion_task():
    logger.info("Tarea para sincronizar recaudación")
    opcion = "01"
    anio = datetime.now().year
    valor = "110659"
    return S42SincronizaRecaudacion(opcion, anio, valor)