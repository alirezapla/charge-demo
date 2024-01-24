from typing import List
from beanie import Document, Indexed
from pydantic import BaseModel, EmailStr, Field
from models.transactions import object_mapper as transaction_mapper
from schemas.transaction import ReadTransaction
from bson import ObjectId


class Customer(Document):
    fullname: str
    email: EmailStr
    phone_number: Indexed(str, unique=True)
    charge_code: str
    transactions: List[ReadTransaction]

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "fullname": "john doe",
                "email": "john@doe.com",
                "phone_number": "09120001122",
                "charge_code": "",
            }
        }
        orm_mode = True

    class Settings:
        name = "customer"


def object_mapper(object: Customer):
    return {
        "id": str(object.id),
        "fullname": object.fullname,
        "email": object.email,
        "phone_number": object.phone_number,
        "charge_code": object.charge_code,
        "transactions": [transaction_mapper(transaction) for transaction in object.transactions],
    }
