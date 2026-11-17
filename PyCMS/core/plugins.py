# core/plugins.py
import importlib.util
import sys
import logging
from pathlib import Path
from types import ModuleType
from typing import Any
from dataclasses import dataclass, field
from core.i18n import _  # Importamos el traductor

# Importamos nuestro sistema de logs centralizado
from core.logger import get_logger

# Obtenemos un logger específico para este módulo
logger = get_logger("Plugins")

# --- MODIFICACIÓN: Crear el espacio de nombres virtual base ---
if "pycms" not in sys.modules:
    # Creamos un módulo vacío llamado 'pycms'
    sys.modules["pycms"] = ModuleType("pycms")
    sys.modules["pycms"].__path__ = [] # Esto le dice a Python que es un "paquete"

if "pycms.plugins" not in sys.modules:
    # Creamos el subpaquete 'pycms.plugins'
    sys.modules["pycms.plugins"] = ModuleType("pycms.plugins")
    sys.modules["pycms.plugins"].__path__ = []
# --------------------------------------------------------------

# Ruta absoluta al directorio de plugins
BASE_DIR = Path(__file__).resolve().parent.parent
PLUGINS_DIR = BASE_DIR / "content" / "plugins"

# Usamos dataclasses para estructurar la información en memoria de cada plugin
@dataclass(slots=True, kw_only=True)
class PluginInfo:
    name: str
    folder_path: Path
    module: ModuleType | None = None
    is_active: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

class PluginManager:
    """
    Gestor centralizado de plugins.
    Responsable de descubrir, cargar, registrar y descargar extensiones del CMS.
    """
    def __init__(self, plugins_dir: Path) -> None:
        self.plugins_dir = plugins_dir
        # Diccionario en memoria para rastrear el estado de todos los plugins
        self._registry: dict[str, PluginInfo] = {}

        if not self.plugins_dir.exists():
            self.plugins_dir.mkdir(parents=True, exist_ok=True)

    def discover_plugins(self) -> None:
        """Solo escanea las carpetas y lee la existencia de plugins, SIN ejecutarlos aún."""
        for plugin_path in self.plugins_dir.iterdir():
            if plugin_path.is_dir() and (plugin_path / "main.py").is_file():
                plugin_name = plugin_path.name
                if plugin_name not in self._registry:
                    self._registry[plugin_name] = PluginInfo(
                        name=plugin_name,
                        folder_path=plugin_path
                    )
        # Usamos logger.info en lugar de print
        logger.info(_("plugins_discovered", count=len(self._registry)))

    def _load_plugin_module(self, plugin_name: str) -> ModuleType | None:
        """
        Responsabilidad Única: Convertir archivos físicos en un módulo de Python en memoria.
        """
        plugin_info = self._registry.get(plugin_name)
        if not plugin_info:
            return None

        entry_point = plugin_info.folder_path / "main.py"
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, entry_point)
            if spec is None or spec.loader is None:
                return None

            module = importlib.util.module_from_spec(spec)
            sys.modules[f"pycms.plugins.{plugin_name}"] = module

            # Ejecutamos el módulo
            spec.loader.exec_module(module)
            return module
        except Exception as e:
            # Usamos logger.error con exc_info=True para el stack trace
            logger.error(f"[ERROR] Falló la carga del módulo '{plugin_name}': {e}", exc_info=True)
            return None

    def activate_plugin(self, plugin_name: str) -> bool:
        """Activa un plugin específico y lo registra como funcional."""
        if plugin_name not in self._registry:
            # Usamos logger.warning para advertencias no críticas
            logger.warning(_("plugin_not_found", name=plugin_name))
            return False

        plugin_info = self._registry[plugin_name]

        if plugin_info.is_active:
            return True # Ya estaba activo

        module = self._load_plugin_module(plugin_name)
        if module:
            plugin_info.module = module
            plugin_info.is_active = True

            # (Opcional) Leer metadatos si el creador del plugin definió __plugin_meta__ en su main.py
            plugin_info.metadata = getattr(module, "__plugin_meta__", {})

            logger.info(_("plugin_loaded", name=plugin_name))
            return True

        return False

    def activate_all(self) -> None:
        """Activa todos los plugins descubiertos. (Ideal para el arranque inicial)"""
        self.discover_plugins()
        for plugin_name in self._registry.keys():
            self.activate_plugin(plugin_name)

# Instancia global para importar en main.py (al igual que hacemos con `hooks`)
plugin_manager = PluginManager(PLUGINS_DIR)
