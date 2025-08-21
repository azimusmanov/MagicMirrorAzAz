from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import select
from app.models.db import get_session
from app.models.model_todo import Todo

router = APIRouter(prefix="/todo", tags=["todo"])
templates = Jinja2Templates(directory="app/ui/templates")

def _render_list(request: Request, session):
    todos = session.exec(select(Todo)).all()
    return templates.TemplateResponse("todo_list.html", {"request": request, "todos": todos})

@router.get("", response_class=JSONResponse)
def list_todos(session=Depends(get_session)):
    # raw JSON (useful for programmatic access / debugging)
    todos = session.exec(select(Todo)).all()
    return todos

@router.get("/partial", response_class=HTMLResponse)
def list_todos_partial(request: Request, session=Depends(get_session)):
    # HTML fragment for HTMX
    return _render_list(request, session)

@router.post("", response_class=HTMLResponse)
def create_todo(
    request: Request,
    title: str = Form(...),
    session=Depends(get_session),
):
    todo = Todo(title=title, done=False)
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return _render_list(request, session)

@router.patch("/{todo_id}", response_class=HTMLResponse)
def update_todo(
    request: Request,
    todo_id: int,
    done: bool,
    session=Depends(get_session)
):
    todo = session.get(Todo, todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Not found")
    todo.done = done
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return _render_list(request, session)
