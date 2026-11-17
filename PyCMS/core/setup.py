# core/setup.py
from pathlib import Path
from core.logger import get_logger

logger = get_logger("Setup")

# Obtenemos el directorio base del proyecto (donde está main.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Definimos los directorios críticos de PyCMS
REQUIRED_DIRECTORIES = [
    BASE_DIR / "content" / "plugins",
    BASE_DIR / "content" / "themes" / "default",  # Aseguramos que exista al menos el tema por defecto
    BASE_DIR / "locales",
    BASE_DIR / "logs",
]

def ensure_directories_exist() -> None:
    """
    Verifica que todos los directorios esenciales para PyCMS existan.
    Si no existen, los crea automáticamente.
    """
    logger.info("Verificando estructura de directorios...")

    for directory in REQUIRED_DIRECTORIES:
        if not directory.exists():
            # parents=True crea las carpetas padre si faltan (ej. crea 'content' y 'plugins')
            # exist_ok=True evita errores si la carpeta ya existe por condición de carrera
            directory.mkdir(parents=True, exist_ok=True)
            logger.info(f"📁 Directorio creado automáticamente: {directory.relative_to(BASE_DIR)}")
        else:
             # Usamos debug para no saturar los logs en cada arranque normal
             logger.debug(f"Directorio verificado: {directory.relative_to(BASE_DIR)}")

    logger.info("✅ Estructura de directorios verificada correctamente.")
