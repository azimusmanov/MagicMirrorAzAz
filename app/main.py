# app/main.py
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from contextlib import asynccontextmanager


from app.models.db import init_db
from app.api.routes_dashboard import router as root_router
from app.api.routes_profiles  import router as profiles_router
from app.api.routes_todo      import router as todo_router
from app.api.routes_ws        import router as ws_router
from app.jobs.scheduler       import start_scheduler
from app.api.routes_dashboard  import weather_router
from sqlmodel import Session, select
from app.models.db import engine
from app.models.model_profile import Profile

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    init_db()
    start_scheduler()
    yield
    # Shutdown code (if any)
    # Example: close_db_connections()

# Load API keys and other secrets
load_dotenv()
app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/ui/static"), name="static")

app.include_router(root_router)
app.include_router(profiles_router)
app.include_router(todo_router)
app.include_router(ws_router)
app.include_router(weather_router)

# Command to run:
# python3 -m app.main
# OR 
# uvicorn app.main:app --reload
if __name__ == '__main__':
    import uvicorn
    import webbrowser
    import threading

    def open_browser():
        webbrowser.open("http://localhost:8000")

    threading.Timer(1.5, open_browser).start()  # Give server time to start
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=False)