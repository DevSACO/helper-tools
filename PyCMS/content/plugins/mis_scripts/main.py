from core.hooks import hooks

def inyectar_seo_head():
    """Esta etiqueta aparecerá dentro del <head> de la página."""
    return '<meta name="generator" content="PyCMS 1.0 (Asíncrono)">\n    <style>body { border-top: 5px solid #3498db; }</style>'

def inyectar_analytics_footer():
    """Este script aparecerá antes de cerrar el </body>."""
    return '<script>console.log("🚀 PyCMS: Scripts inyectados correctamente vía plugin.");</script>'

# Colgamos nuestras funciones en los ganchos correspondientes
hooks.add_action('wp_head', inyectar_seo_head, priority=10)
hooks.add_action('wp_footer', inyectar_analytics_footer, priority=20)
