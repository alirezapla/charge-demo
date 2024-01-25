import services.consumer as consumer
import uvicorn
from controller.charge import router
from core.config import initiate_database
from fastapi import FastAPI
from fastapi_amis_admin.admin.settings import Settings
from fastapi_amis_admin.admin.site import AdminSite
from fastapi_scheduler import SchedulerAdmin
from services.scheduler import (check_newst_records_scheduler,
                                update_customer_service_scheduler)

VERSION = "0.0.1"
TITLE = "charge"

app = FastAPI(title=TITLE, version=VERSION)

app.include_router(router, tags=["Charge"], prefix="/charge")
site = AdminSite(
    settings=Settings(database_url_async="sqlite+aiosqlite:///amisadmin.db", language="en_US")
)

scheduler = SchedulerAdmin.bind(site)


@scheduler.scheduled_job("interval", seconds=30)
async def interval_check_newst_records_scheduler():
    await check_newst_records_scheduler()


@scheduler.scheduled_job("interval", seconds=60)
async def interval_update_customer_service_schedulert():
    await update_customer_service_scheduler()


site.mount_app(app)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome To charge service"}


################### Event Handlers ###################


@app.on_event("startup")
async def start_database():
    consumer.loop()
    await initiate_database()
    scheduler.start()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5002, reload=True, log_level="debug")
