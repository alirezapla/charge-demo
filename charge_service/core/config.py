import os
from functools import lru_cache
from pydantic_settings import BaseSettings
from enum import Enum
from decouple import config
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
import models as models


class Environment(Enum):
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


class Settings:
    APP_NAME: str = "charge"
    APP_VERSION: str = "0.1.0"
    DB_DEBUG: bool = False
    MONGODB_DB_URL = config("MONGO_CLIENT")


async def initiate_database():
    client = AsyncIOMotorClient(Settings().MONGODB_DB_URL)
    await init_beanie(database=client.get_default_database(), document_models=models.__all__)


@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": Settings,
    }
    config_name = os.environ.get("CELERY_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()
