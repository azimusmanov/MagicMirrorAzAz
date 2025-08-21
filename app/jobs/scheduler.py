from apscheduler.schedulers.asyncio import AsyncIOScheduler

# create a global scheduler instance
scheduler = AsyncIOScheduler()

def start_scheduler():
    """Start the scheduler if it isn't already running."""
    if not scheduler.running:
        scheduler.start()

# later you’ll add things like:
# scheduler.add_job(some_function, "interval", minutes=30)
