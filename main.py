from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from fastapi import FastAPI

import models  # noqa
from database import Base, engine
from resources import exchange_rates
from utils.exchange_rate import fetch_and_store_exchange_rates

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


scheduler.add_job(
    fetch_and_store_exchange_rates,
    CronTrigger(hour=0, minute=2),
    id='daily_task',
    replace_existing=True,
)


Base.metadata.create_all(bind=engine)


@app.get('/')
async def health_check():
    return {'message': 'System is up and running'}


app.include_router(exchange_rates.router)
