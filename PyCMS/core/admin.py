# core/admin.py
from fastapi import APIRouter, Request, Form, Path, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

# Asumiendo que tu crud actualizado ya está disponible
from core.crud import get_all_posts, get_post_by_slug, get_post_by_id, delete_post, create_post, update_post

# Alias de tipos modernos para hacer las firmas más limpias (Python 3.12+)
type HTML = HTMLResponse
type Redirect = RedirectResponse

admin_router = APIRouter(prefix="/admin", tags=["admin"])
admin_templates = Jinja2Templates(directory="core/admin/templates")

@admin_router.get("/posts", response_class=HTMLResponse)
async def list_posts(request: Request) -> HTML:
    """Pantalla equivalente a wp-admin/edit.php"""
    posts = await get_all_posts()
    return admin_templates.TemplateResponse(
        request=request,
        name="posts.html",
        context={"posts": posts}
    )

@admin_router.get("/post-create", response_class=HTMLResponse)
async def new_post_form(request: Request) -> HTML:
    """Muestra el formulario HTML del editor."""
    return admin_templates.TemplateResponse(
        request=request,
        name="editor.html",
        context={}
    )

@admin_router.post("/post-create")
async def save_new_post(
    request: Request,
    title: str = Form(...),
    slug: str = Form(...),
    content: str = Form(""),
    post_type: str = Form("post"),
    blocks_json: str = Form("{}")
) -> Redirect:
    """Recibe los datos del formulario y los guarda en PostgreSQL."""

    # Podríamos usar TaskGroup si tuvieras más tareas paralelas aquí
    await create_post(title, slug, content, post_type, blocks_json)

    # Redirigimos al usuario a la página pública del post recién creado
    return RedirectResponse(url=f"/{slug}", status_code=303)

@admin_router.get("/post-edit/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int = Path(...)) -> HTML:
    """Carga el formulario pre-llenado con los datos del post."""
    post = await get_post_by_id(post_id)

    # Usando Pattern Matching para validar y extraer
    match post:
        case None:
            raise HTTPException(status_code=404, detail="El post no existe en la base de datos.")
        case valid_post:
            return admin_templates.TemplateResponse(
                request=request,
                name="edit.html",
                context={"post": valid_post}
            )

@admin_router.post("/post-edit/{post_id}")
async def handle_edit_post(
    request: Request,
    post_id: int = Path(...),
    title: str = Form(...),
    slug: str = Form(...),
    content: str = Form(""),
    post_type: str = Form(...),
    blocks_json: str = Form("{}")
) -> Redirect:
    """Actualiza los datos de un post existente."""
    success = await update_post(post_id, title, slug, content, post_type, blocks_json)

    match success:
        case False:
            raise HTTPException(status_code=404, detail="Error al actualizar. Post no encontrado.")
        case True:
             # Redirigimos al usuario a la página de administración de los post creados
            return RedirectResponse(url="/admin/posts", status_code=303)

@admin_router.post("/post-delete/{post_id}")
async def handle_delete_post(post_id: int = Path(...)) -> Redirect:
    """Recibe la orden de borrar desde un botón form y redirige a la lista"""
    success = await delete_post(post_id)

    match success:
        case False:
             raise HTTPException(status_code=404, detail="No se pudo eliminar el post.")
        case True:
            # Status 303 indica que la redirección POST a GET fue exitosa
            return RedirectResponse(url="/admin/posts", status_code=303)
