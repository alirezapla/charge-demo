from typing import Optional, Any, List
from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId


class Transaction(BaseModel):
    amount: float
    description: str


class CreateCustomerModel(BaseModel):
    fullname: str
    email: EmailStr
    phone_number: str
    charge_code: str

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


class UpdateCustomerModel(BaseModel):
    fullname: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    charge_code: Optional[str] = None

    class Collection:
        name = "customer"

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {
            "example": {
                "fullname": "john doe",
                "email": "john@doe.com",
                "phone_number": "09120001122",
            }
        }


class AddTransactionCustomerModel(BaseModel):
    transactions: List[Transaction] = None

    class Collection:
        name = "customer"

    class Config:
        arbitrary_types_allowed = True
        schema_extra = {"example": {"transactions": []}}


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
