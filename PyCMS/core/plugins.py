import importlib.util
from pathlib import Path
import sys

# Ruta absoluta al directorio de plugins
BASE_DIR = Path(__file__).resolve().parent.parent
PLUGINS_DIR = BASE_DIR / "content" / "plugins"

def load_all_plugins():
    """Escanea y carga dinámicamente todos los plugins activos."""

    if not PLUGINS_DIR.exists():
        print("El directorio de plugins no existe.")
        return

    # Iterar sobre cada elemento en el directorio de plugins
    for plugin_path in PLUGINS_DIR.iterdir():
        # Validar que sea un directorio y contenga el archivo main.py
        if plugin_path.is_dir():
            entry_point = plugin_path / "main.py"

            if entry_point.exists():
                plugin_name = plugin_path.name

                try:
                    # 1. Crear la especificación del módulo desde la ruta del archivo
                    spec = importlib.util.spec_from_file_location(plugin_name, entry_point)

                    # 2. Crear el módulo a partir de la especificación
                    module = importlib.util.module_from_spec(spec)

                    # (Opcional) Añadir el módulo a sys.modules para poder importarlo desde otros lados
                    sys.modules[f"plugins.{plugin_name}"] = module

                    # 3. Ejecutar el módulo (esto corre el código del plugin y registra los hooks)
                    spec.loader.exec_module(module)

                    print(f"[OK] Plugin cargado: {plugin_name}")
                except Exception as e:
                    print(f"[ERROR] Falló la carga del plugin '{plugin_name}': {e}")
