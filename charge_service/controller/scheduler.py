# from fastapi import APIRouter, Body
# from services.charge import retrive_record, update_records_checked_flag
# from schema import Response, CodeActivationResult
# from exceptions.http_exceptions import BadRequest
# from main import scheduler

# router = APIRouter()


# @router.get("/start", response_description="start scheduler", response_model=Response)
# async def get_newst_records():
#     scheduler.start()


# def response_handler(object):
#     if object:
#         if isinstance(object, BadRequest):
#             return {
#                 "status_code": 400,
#                 "response_type": "error",
#                 "description": "customer with ID: {} updated".format(id),
#                 "data": str(object),
#             }
#         return {
#             "status_code": 200,
#             "response_type": "success",
#             "description": "customer with ID: {} updated".format(id),
#             "data": object,
#         }
#     return {
#         "status_code": 404,
#         "response_type": "error",
#         "description": "An error occurred. customer with ID: {} not found".format(id),
#         "data": False,
#     }
