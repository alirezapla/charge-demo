import random
from datetime import datetime

from pydantic import BaseModel, Field


class ChargeCodeRequest(BaseModel):
    phone_number: str
    charge_code: str


class ChargeRecord(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    label: bool
    id: str
