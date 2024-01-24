from fastapi import APIRouter, Body
from services.charge import retrive_record, update_records_checked_flag
from schema import Response, CodeActivationResult
from exceptions.http_exceptions import BadRequest

router = APIRouter()


@router.get("/newst", response_description="records retrieved", response_model=Response)
async def get_newst_records(limit_number: int):
    customers = await retrive_record(limit_number)
    return response_handler(customers)


@router.put("/checked", response_description="records checked", response_model=Response)
async def update(body: list[CodeActivationResult]):
    customers = await update_records_checked_flag(body)
    return response_handler(customers)


def response_handler(object):
    if object:
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
