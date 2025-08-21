from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.weather import fetch_weather

templates = Jinja2Templates(directory="app/ui/templates")
router = APIRouter()
weather_router = APIRouter(prefix="/weather", tags=["weather"])


@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@weather_router.get("/partial", response_class=HTMLResponse)
def weather_partial(request: Request):
    data = fetch_weather()
    return templates.TemplateResponse("weather_widget.html", {"request": request, "w": data})
