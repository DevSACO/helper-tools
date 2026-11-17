# core/logger.py
import logging
import sys
from pathlib import Path

# Definimos la ruta para guardar los logs en un archivo
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"

def setup_logging() -> None:
    """
    Configura el sistema de logging centralizado para PyCMS.
    Debe llamarse lo antes posible en el ciclo de vida de la aplicación.
    """
    # Creamos el directorio de logs si no existe
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    log_file = LOGS_DIR / "pycms.log"

    # Definimos el formato de los mensajes de log
    # Ejemplo: 2026-11-17 07:34:00 - INFO - PyCMS.Plugins - [OK] Plugin cargado: seo_tools
    log_format = logging.Formatter(
        fmt="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Manejador para enviar logs a la consola (terminal)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(log_format)

    # Manejador para enviar logs a un archivo (útil para producción)
    # FileHandler asegura que los logs persistan tras reiniciar el servidor
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(log_format)

    # Obtenemos el logger "raíz" de nuestra aplicación
    root_logger = logging.getLogger("PyCMS")
    root_logger.setLevel(logging.INFO) # Nivel mínimo de severidad a registrar

    # Limpiamos manejadores previos por si la función se llama múltiples veces (ej. recargas en dev)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Añadimos nuestros manejadores al logger raíz
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    # También podemos configurar el nivel de loggers de terceros si son muy ruidosos
    # Ejemplo: logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

# Instancia conveniente para obtener loggers de subsistemas específicos
def get_logger(module_name: str) -> logging.Logger:
    """Retorna un logger con el prefijo 'PyCMS.'"""
    return logging.getLogger(f"PyCMS.{module_name}")
