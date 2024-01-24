from datetime import datetime
from typing import List
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class Charge(Document):
    phone_number_code: Indexed(str, unique=True)
    timestamp: datetime
    transaction_id: str
    checked_label: bool
    working_label: bool
    activated_label: bool

    class Config:
        arbitrary_types_allowed = True

        orm_mode = True

    class Settings:
        name = "charge"


def object_mapper(object: Charge):
    return {
        "phone_number_code": object.phone_number_code,
        "timestamp": object.timestamp,
        "transaction_id": object.transaction_id,
    }


# def object_mapper(object: Charge):
#     return {
#         "id": str(object.id),
#         "phone_number_code": object.phone_number_code,
#         "timestamp": object.timestamp,
#         "transaction_id": object.transaction_id,
#         "checked_label": object.checked_label,
#         "working_label": object.working_label,
#         "activated_label": object.activated_label,
#     }
