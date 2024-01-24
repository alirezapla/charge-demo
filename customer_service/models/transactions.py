from typing import Optional, Any
from datetime import datetime
from beanie import Document
from pydantic import BaseModel, Field
from bson import ObjectId


class Transaction(Document):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    amount: float
    description: str
    timestamp: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {ObjectId: str, datetime: lambda dt: dt.isoformat()}

        arbitrary_types_allowed = True


def object_mapper(object: Transaction):
    return {
        "amount": object.amount,
        "description": object.description,
        "timestamp": object.timestamp,
    }
