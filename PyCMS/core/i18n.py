# core/i18n.py
import json
from pathlib import Path
from typing import Any
from contextvars import ContextVar
from core.logger import get_logger

logger = get_logger("i18n")

BASE_DIR = Path(__file__).resolve().parent.parent
LOCALES_DIR = BASE_DIR / "locales"

# 🚀 MAGIA AQUÍ: Esta variable es única para cada petición (usuario)
current_lang: ContextVar[str] = ContextVar("current_lang", default="es")

class Translator:
    """Gestor de Internacionalización (i18n) para PyCMS"""

    def __init__(self, default_lang: str = "es") -> None:
        self.default_lang = default_lang
        # Ahora guardamos un diccionario de diccionarios: {"es": {...}, "en": {...}}
        self.translations: dict[str, dict[str, str]] = {}
        self.load_all_translations()

    def load_all_translations(self) -> None:
        """Carga TODOS los archivos JSON de idiomas en memoria al arrancar."""
        if not LOCALES_DIR.exists():
            LOCALES_DIR.mkdir(parents=True, exist_ok=True)
            return

        for lang_file in LOCALES_DIR.glob("*.json"):
            lang_code = lang_file.stem # Ej: de "es.json" extrae "es"
            try:
                with open(lang_file, "r", encoding="utf-8") as f:
                    self.translations[lang_code] = json.load(f)
                logger.debug(f"Traducciones cargadas para: {lang_code}")
            except json.JSONDecodeError as e:
                logger.error(f"Error al leer {lang_file.name}: {e}")

    def t(self, key: str, **kwargs: Any) -> str:
        """Obtiene la traducción basándose en el idioma de la petición actual."""
        # Obtenemos el idioma del usuario actual
        lang = current_lang.get()

        # Buscamos en su idioma. Si no existe, usamos el idioma por defecto ("es")
        lang_dict = self.translations.get(lang, self.translations.get(self.default_lang, {}))

        text = lang_dict.get(key, key)

        if kwargs:
            try:
                return text.format(**kwargs)
            except KeyError:
                return text

        return text


# Instancia global (Puedes cambiar "es" leyendo una variable de entorno como os.getenv("PYCMS_LANG"))
translator = Translator()

# Alias ultra-corto estándar en la industria para traducciones
_ = translator.t
