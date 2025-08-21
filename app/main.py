# app/main.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

from app.models.db import init_db
from app.api.routes_dashboard import router as root_router
from app.api.routes_profiles  import router as profiles_router
from app.api.routes_todo      import router as todo_router
from app.api.routes_ws        import router as ws_router
from app.jobs.scheduler       import start_scheduler

load_dotenv()
app = FastAPI(title="Magic Mirror (Stage 0)")
app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")

app.include_router(root_router)
app.include_router(profiles_router)
app.include_router(todo_router)
app.include_router(ws_router)

@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()
