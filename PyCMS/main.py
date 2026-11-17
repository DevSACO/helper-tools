# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates

from core.admin import admin_router
from core.plugins import plugin_manager # Usando nuestro nuevo gestor
from core.crud import get_post_by_slug
from core.i18n import current_lang
from core.hooks import hooks
from core.db import engine, Base
from core.logger import setup_logging, get_logger
from core.setup import ensure_directories_exist # Importamos la nueva función

# Configuramos el logging antes de hacer cualquier otra cosa
setup_logging()

# Obtenemos un logger para el archivo principal
logger = get_logger("Core")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Se ejecuta una sola vez al arrancar el servidor (y al apagarlo).
    Es el lugar perfecto para cargar los plugins en memoria y conectar servicios.
    """
    # Reemplazamos print por logger.info
    logger.info("🚀 Arrancando PyCMS...")
    # Aseguramos que la estructura de carpetas existe
    ensure_directories_exist()

    # Crear las tablas en PostgreSQL si no existen
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("✅ Tablas de base de datos verificadas/creadas.")

    # Cargamos todos los plugins activos. Ellos registrarán sus funciones en los hooks.
    plugin_manager.activate_all()

    # Ejecutamos un hook de inicio, por si algún plugin necesita hacer algo al arrancar
    hooks.do_action('cms_init')

    yield # Aquí el CMS se queda corriendo recibiendo peticiones

    logger.info("🛑 Apagando PyCMS...")
    # Hook de apagado (ej. para cerrar conexiones personalizadas de plugins)
    hooks.do_action('cms_shutdown')

# Inicializamos el framework
app = FastAPI(title="PyCMS", lifespan=lifespan)

@app.middleware("http")
async def language_middleware(request: Request, call_next):
    """
    Este middleware se ejecuta en CADA petición que recibe PyCMS.
    Detecta el idioma del visitante y lo guarda en su contexto local.
    """
    # 1. Estrategia 1: Parámetro en la URL (ej: misitio.com/?lang=en)
    lang = request.query_params.get("lang")
    
    # 2. Estrategia 2: Cabecera del navegador (Accept-Language)
    if not lang:
        accept_lang = request.headers.get("Accept-Language", "")
        if accept_lang:
            # Los navegadores envían algo como: "es-ES,es;q=0.9,en;q=0.8"
            # Extraemos el primer idioma principal ("es")
            lang = accept_lang.split(",")[0].split("-")[0]
    
    # 3. Si no detectamos nada, usamos español por defecto
    if not lang:
        lang = "es"
        
    # Establecemos el idioma para ESTA petición asíncrona
    token = current_lang.set(lang)
    
    # Procesamos la petición (FastAPI hace su magia aquí, llamando a rutas, Jinja, etc.)
    response = await call_next(request)
    
    # Limpiamos el contexto al terminar (Buena práctica de memoria)
    current_lang.reset(token)
    
    return response

# --- INCLUIMOS EL PANEL DE ADMINISTRACIÓN ---
app.include_router(admin_router)

# Configuramos el motor de plantillas apuntando a nuestra carpeta de temas
templates = Jinja2Templates(directory="content/themes")
admin_templates = Jinja2Templates(directory="core/admin/templates")

# Inyectamos la función _() para que esté disponible en CUALQUIER plantilla HTML
templates.env.globals["_"] = _
admin_templates.env.globals["_"] = _

# Inyectar funciones globales al estilo WordPress ---
templates.env.globals["wp_head"] = lambda: hooks.do_action_to_string("wp_head")
templates.env.globals["wp_footer"] = lambda: hooks.do_action_to_string("wp_footer")

# Definimos una ruta que capture cualquier path, ej: midominio.com/mi-primer-post
# Usamos {slug:path} para que también capture URLs con subniveles (ej: /categoria/mi-post)
@app.get("/{slug:path}")
async def serve_page(request: Request, slug: str):
    # 1. Si la URL es la raíz ("/") el slug llegará vacío. Le asignamos el slug del home.
    if not slug:
        slug = "home"

    # 2. Intentamos interceptar el slug mediante un filtro por si un plugin quiere cambiarlo
    # (Ejemplo: un plugin de redirecciones 301)
    slug = hooks.apply_filters('request_slug', slug)

    # 3. Vamos a nuestra capa de caché/PostgreSQL a buscar el contenido
    post_data = await get_post_by_slug(slug)

    # 4. Manejo del error 404 (Not Found)
    if not post_data:
        raise HTTPException(status_code=404, detail="El contenido no existe o no está publicado.")

    # 5. Interceptamos los datos del post antes de imprimirlos
    # Un plugin de SEO podría inyectar metadatos aquí, o uno de censura ofuscar palabras.
    post_data = hooks.apply_filters('the_post_data', post_data)

    # Pasar este post_data a un tema HTML.
    active_theme = "default"
    theme_route = f"content/themes/{active_theme}"

    # 1. Definimos qué plantilla buscar según el tipo de post
    publish_type = post_data.get('post_type', 'post')
    if publish_type == 'page':
        main_template = "page.html"
    elif publish_type == 'post':
        main_template = "single.html"
    else:
        # Para Custom Post Types (ej: portfolio -> single-portfolio.html)
        main_template = f"single-{publish_type}.html"

    # 2. Comprobamos si el archivo existe; si no, usamos index.html (Fallback)
    last_template = "index.html"
    if os.path.exists(f"{theme_route}/{main_template}"):
        last_template = main_template

    # 3. Filtro equivalente a 'template_include' en WordPress
    last_template = hooks.apply_filters('template_include', last_template, post_data)

    # 4. Renderizamos usando la plantilla elegida dinámicamente
    return templates.TemplateResponse(
        request=request,
        name=f"{active_theme}/{last_template}",
        context={"post": post_data}
    )
