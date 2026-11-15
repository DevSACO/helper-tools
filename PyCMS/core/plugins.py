# core/plugins.py
import importlib.util
import sys
import logging
from pathlib import Path
from types import ModuleType

# Configuración básica de logging (recomendado en lugar de usar `print` en producción)
logger = logging.getLogger("PyCMS.Plugins")
logger.setLevel(logging.INFO)

# Ruta absoluta al directorio de plugins
BASE_DIR = Path(__file__).resolve().parent.parent
PLUGINS_DIR = BASE_DIR / "content" / "plugins"

def _load_plugin_module(plugin_name: str, entry_point: Path) -> ModuleType | None:
    """
    Función auxiliar para cargar un módulo individualmente.
    Retorna el módulo cargado o None si ocurre un error.
    """
    try:
        # 1. Crear la especificación del módulo desde la ruta del archivo
        spec = importlib.util.spec_from_file_location(plugin_name, entry_point)

        # Validamos que el spec y el loader existan para complacer a los type checkers
        if spec is None or spec.loader is None:
             logger.warning(f"[WARN] No se pudo generar la especificación para el plugin: {plugin_name}")
             return None

        # 2. Crear el módulo a partir de la especificación
        module = importlib.util.module_from_spec(spec)

        # 3. Añadir el módulo a sys.modules con un prefijo seguro
        # Esto permite que un plugin importe archivos de su propia carpeta si lo necesita
        module_identifier = f"pycms.plugins.{plugin_name}"
        sys.modules[module_identifier] = module

        # 4. Ejecutar el módulo (esto corre el código del plugin y registra los hooks)
        spec.loader.exec_module(module)

        return module
    except Exception as e:
        # Aquí Python 3.11+ (y por ende 3.15) incluye el traceback mejorado automáticamente
        logger.error(f"[ERROR] Falló la carga del plugin '{plugin_name}': {e}", exc_info=True)
        return None

def load_all_plugins() -> None:
    """
    Escanea el directorio de plugins y carga dinámicamente aquellos que sean válidos.
    """
    if not PLUGINS_DIR.exists():
        logger.warning(f"[WARN] El directorio de plugins no existe: {PLUGINS_DIR}")
        # Lo creamos automáticamente para que el usuario no tenga que hacerlo a mano
        PLUGINS_DIR.mkdir(parents=True, exist_ok=True)
        return

    loaded_count = 0

    # Iterar usando iterdir() que es rápido y eficiente
    for plugin_path in PLUGINS_DIR.iterdir():
        # Validar que sea un directorio y contenga el archivo main.py
        if plugin_path.is_dir():
            entry_point = plugin_path / "main.py"

            if entry_point.is_file():
                plugin_name = plugin_path.name

                # Cargamos el plugin
                if _load_plugin_module(plugin_name, entry_point):
                    logger.info(f"[OK] Plugin cargado: {plugin_name}")
                    loaded_count += 1
            else:
                 logger.debug(f"Directorio ignorado (sin main.py): {plugin_path.name}")

    logger.info(f"🚀 PyCMS finalizó la carga de plugins. Total cargados: {loaded_count}")
