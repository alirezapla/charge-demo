from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any


class ChargeCodeRequest(BaseModel):
    phone_number: str
    charge_code: str


class ChargeRecord(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    label: bool
    id: str


class DispatcherMessage(BaseModel):
    transaction_id: str
    phone_number_code: str
    timestamp: datetime


class CodeActivationResult(BaseModel):
    phone_number_code: str
    activated: bool


class Response(BaseModel):
    status_code: int
    response_type: str
    description: str
    data: Optional[Any]

    class Config:
        schema_extra = {
            "example": {
                "status_code": 200,
                "response_type": "success",
                "description": "Operation successful",
                "data": "Sample data",
            }
        }
