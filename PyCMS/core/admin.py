# core/admin.py
from fastapi import APIRouter, Request, Form, Path
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from core.crud import get_all_posts, delete_post, create_post
from core.crud import get_all_posts, get_post_by_slug , get_post_by_id, delete_post, create_post, update_post

# Creamos un router exclusivo para todo lo que empiece con /admin
admin_router = APIRouter(prefix="/admin", tags=["admin"])
admin_templates = Jinja2Templates(directory="core/admin/templates")

@admin_router.get("/post-create", response_class=HTMLResponse)
async def new_post_form(request: Request):
    """Muestra el formulario HTML del editor."""
    return admin_templates.TemplateResponse(
        request=request,
        name="editor.html",
        context={}
    )

@admin_router.get("/post-edit/{post_id}", response_class=HTMLResponse)
async def edit_post_form(request: Request, post_id: int = Path(...)):
    """Carga el formulario pre-llenado con los datos del post."""
    post = await get_post_by_id(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="El post no existe en la base de datos.")

    return admin_templates.TemplateResponse(
        request=request,
        name="edit.html",
        context={"post": post}
    )

@admin_router.get("/posts", response_class=HTMLResponse)
async def list_posts(request: Request):
    """Pantalla equivalente a wp-admin/edit.php"""
    posts = await get_all_posts()
    return admin_templates.TemplateResponse(
        request=request,
        name="posts.html",
        context={"posts": posts}
    )

@admin_router.post("/post-create")
async def save_new_post(
    request: Request,
    title: str = Form(...),
    slug: str = Form(...),
    content: str = Form(""),
    post_type: str = Form("post"),
    blocks_json: str = Form("{}")
):

    """Recibe los datos del formulario y los guarda en PostgreSQL."""
    await create_post(title, slug, content, post_type, blocks_json)
    # Redirigimos al usuario a la página pública del post recién creado
    return RedirectResponse(url=f"/{slug}", status_code=303)

@admin_router.post("/post-edit/{post_id}")
async def handle_edit_post(
    request: Request,
    post_id: int = Path(...),
    title: str = Form(...),
    slug: str = Form(...),
    content: str = Form(""),
    post_type: str = Form(...),
    blocks_json: str = Form("{}")
):
    await update_post(post_id, title, slug, content, post_type, blocks_json)
    # Redirigimos al usuario a la página de administración de los post creados
    return RedirectResponse(url="/admin/posts", status_code=303)

@admin_router.post("/post-delete/{post_id}")
async def handle_delete_post(post_id: int = Path(...)):
    """Recibe la orden de borrar desde un botón form y redirige a la lista"""
    await delete_post(post_id)
    # Status 303 indica que la redirección POST a GET fue exitosa
    return RedirectResponse(url="/admin/posts", status_code=303)
