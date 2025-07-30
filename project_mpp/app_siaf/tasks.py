from celery import shared_task
from celery.utils.log import get_task_logger
from django.core.cache import cache
from app_siaf.siaf_token_manager import SIAFTokenManager

logger = get_task_logger(__name__)

@shared_task
def add(x, y):
    # crear un archivo con el nombre de la tarea y el resultado
    with open('task_result.txt', 'w') as f:
        f.write(f'El resultado de la tarea {x} + {y} = {x + y}')
    return x + y

@shared_task
def set_cache(key, value):
    """Tarea simple para guardar un valor en cache"""
    cache.set(key, value, timeout=300)  # 5 minutos
    return f"Valor '{value}' guardado en cache con key '{key}'"

@shared_task
def get_siaf_token_task():
    logger.info("Tarea para obtener token de SIAF")
    siaf_token_manager = SIAFTokenManager()    
    return siaf_token_manager.get_access_token()

@shared_task
def sample_task():
    logger.info("Ejecutando tarea de prueba")
    return "Sample task ejecutada correctamente"