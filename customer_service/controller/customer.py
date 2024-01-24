from fastapi import APIRouter, Body

from services.repository import *
from models.customer import *
from schemas.customer import (
    CreateCustomerModel,
    UpdateCustomerModel,
    Response,
    AddTransactionCustomerModel,
)
from exceptions.customer_exceptions import BadRequest

router = APIRouter()


@router.get("/", response_description="Customers retrieved", response_model=Response)
async def get_customers(limit_number: int):
    customers = await retrieve_customers(limit_number)
    return response_handler(customers)


@router.get("/{id}", response_description="Customer data retrieved", response_model=Response)
async def get_customer_data(id: PydanticObjectId):
    customer = await retrieve_customer(id)
    return response_handler(customer)


@router.get(
    "/by-phone/{phone_number}",
    response_description="Customer data retrieved",
    response_model=Response,
)
async def get_customer_data_by_phone_number(phone_number: str):
    customer = await retrieve_customer_by_phone(phone_number)
    return response_handler(customer)


@router.post(
    "/bulk/phones",
    response_description="Group of customers data retrieved",
    response_model=Response,
)
async def get_group_customers_data(phone_numbers: list[str]):
    customer = await retrieve_group_customers(phone_numbers)
    return response_handler(customer)


@router.put(
    "/bulk/activate-code/{code}",
    response_description="Group of customers data retrieved",
    response_model=Response,
)
async def get_group_customers_data(phone_numbers: list[str], code: str):
    customer = await update_group_customers(phone_numbers, code)
    return response_handler(customer)


@router.get(
    "/{id}/balance", response_description="Customer balance retrieved", response_model=Response
)
async def get_customer_balance(id: PydanticObjectId):
    customer_balance = await retrieve_customer_balance(id)
    return response_handler(customer_balance)


@router.get(
    "/{code}/count", response_description="Number of code activated", response_model=Response
)
async def get_number_of_active_code(code: str):
    count = await retrieve_activated_code_count(code)
    return response_handler(count)


@router.post(
    "/",
    response_description="customer data added into the database",
    response_model=Response,
)
async def add_customer_data(customer: CreateCustomerModel = Body(...)):
    new_customer = await add_customer(customer)
    return response_handler(new_customer)


@router.delete("/{id}", response_description="customer data deleted from the database")
async def delete_customer_data(id: PydanticObjectId):
    deleted_customer = await delete_customer(id)
    return response_handler(deleted_customer)


@router.put("/{id}", response_model=Response)
async def update_customer(id: PydanticObjectId, req: UpdateCustomerModel = Body(...)):
    updated_customer = await update_customer_data(id, req.dict())
    return response_handler(updated_customer)


@router.put("/add_transaaction/{id}", response_model=Response)
async def add_transaction_customer(
    id: PydanticObjectId, req: AddTransactionCustomerModel = Body(...)
):
    updated_customer = await add_transaction_to_customer_transactions(id, req)
    return response_handler(updated_customer)


def response_handler(object):
    if object or ((isinstance(object, dict) or isinstance(object, list)) and len(object) == 0):
        if isinstance(object, BadRequest):
            return {
                "status_code": 400,
                "response_type": "error",
                "description": "customer with ID: {} updated".format(id),
                "data": str(object),
            }
        return {
            "status_code": 200,
            "response_type": "success",
            "description": "customer with ID: {} updated".format(id),
            "data": object,
        }
    return {
        "status_code": 404,
        "response_type": "error",
        "description": "An error occurred. customer with ID: {} not found".format(id),
        "data": False,
    }
