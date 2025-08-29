from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.services.weather import fetch_weather
from app.services.quotes import get_daily_quote
from app.services.news import get_news_headlines


templates = Jinja2Templates(directory="app/ui/templates")
router = APIRouter()
weather_router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Daily Weather Route
@weather_router.get("/partial", response_class=HTMLResponse)
def weather_partial(request: Request):
    data = fetch_weather()
    return templates.TemplateResponse("weather_widget.html", {"request": request, "w": data})

# Daily Quote Route
@router.get("/quotes/partial", response_class=HTMLResponse)
def quotes_partial(request: Request):
    quote = get_daily_quote()
    return templates.TemplateResponse(
        "quote_widget.html", {"request": request, "quote": quote}
    )

# Daily News Route
@router.get("/news/partial", response_class=HTMLResponse)
def news_partial(request: Request):
    headlines = get_news_headlines(5)  # Get 5 headlines
    return templates.TemplateResponse(
        "news_widget.html", {"request": request, "headlines": headlines}
    )