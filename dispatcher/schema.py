from pydantic import BaseModel, Field
from datetime import datetime
import random


class ChargeCodeRequest(BaseModel):
    phone_number: str
    charge_code: str


class ChargeRecord(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    label: bool
    id: str
