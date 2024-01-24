from typing import Optional, Any
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field
from bson import ObjectId


class Transaction(BaseModel):
    id: ObjectId
    amount: float
    description: str
    timestamp: datetime

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

        arbitrary_types_allowed = True


class ReadTransaction(BaseModel):
    amount: float
    description: str
    timestamp: datetime

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

        arbitrary_types_allowed = True


class CreateTransaction(BaseModel):
    amount: float
    description: str


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


def object_mapper(object: Transaction):
    return {
        "amount": object.amount,
        "description": object.description,
        "timestamp": object.timestamp,
    }
