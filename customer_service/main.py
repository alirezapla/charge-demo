import uvicorn
from config.config import initiate_database
from controller.customer import router as CustomerRouter
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
async def start_database():
    await initiate_database()


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to this account service."}


# app.include_router(, tags=["Administrator"], prefix="/admin")
app.include_router(CustomerRouter, tags=["Customer"], prefix="/customer")


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True, log_level="debug")
