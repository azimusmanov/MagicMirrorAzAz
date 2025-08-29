# MagicMirrorAzAz

This is an early test project for my custom magic mirror. This repository houses all the code necessary for the project, along with any other dependencies. I've decided not to use existing Magic Mirror Modules (for now), instead opting to recreate most modules from scratch. This approach is primarily for my own learning and to enable more efficient backend interactions.

I am currently still in the early stages, designing and implementing the mirror functionality. After I get back to campus, I plan to order the parts and physically construct the mirror.

## Overview

This project is a modular FastAPI web application for a personal dashboard ("Magic Mirror"). It features user profiles, a to-do list, weather widgets, quotes, and news headlines. The backend uses SQLModel for database models and APScheduler for scheduled jobs. The frontend is rendered with Jinja2 templates and supports dynamic updates via HTMX and JavaScript.

## Key Components

- `main.py`: FastAPI app entry point; mounts static files, includes routers, initializes the database, seeds a default profile, and starts the scheduler.
- `api/`: Contains routers for dashboard (`routes_dashboard.py`), profiles (`routes_profiles.py`), todos (`routes_todo.py`), and WebSocket events (`routes_ws.py`).
- `models/`: SQLModel-based ORM models for profiles, todos, and widget state. `db.py` sets up the database engine and session.
- `services/`: Service modules for weather, quotes, news, and location.
- `jobs/scheduler.py`: Sets up APScheduler for background jobs.
- `ui/templates/`: Jinja2 HTML templates for dashboard, weather, and todo list.
- `ui/static/`: Static assets (CSS, JS, images).

## How It Works

- On startup, the app initializes the database and seeds a default profile if none exists.
- The dashboard displays profile info, to-do list, weather widget, quotes, and news.
- Widgets update dynamically using HTMX with configurable refresh intervals.
- WebSocket endpoint (`/ws/events`) is ready for future real-time event streaming.
- Profiles can be switched and managed via API endpoints.

## Running the App

1. Install dependencies
2. Set environment variables in a `.env` file (e.g., `OPENWEATHER_API_KEY`, `NEWS_API_KEY`)
3. Start the server:
uvicorn app.main:app --reload
OR
python3 -m app.main

