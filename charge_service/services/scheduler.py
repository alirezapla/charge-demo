import httpx
from decouple import config
from services.charge import (retrive_activated_records, retrive_records_phone,
                             soft_delete_records, update_records_checked_flag)

from common import MyLogger

logger = MyLogger()
CODE = config("CHARGE_CODE")
LIMIT = int(config("CHARGE_CODE_LIMIT"))
BATCH_SIZE = int(config("BATCH_SIZE"))
CUSTOMER_SERVICE = config("CUSTOMER_SERVICE")
HEADERS = {"accept": "application/json", "Content-Type": "application/json"}


async def check_newst_records_scheduler():
    logger.info("", "CHECK_RECORDS_SCHEDULER_STARTED", "check_newst_records")
    phones = await retrive_records_phone(BATCH_SIZE)
    if len(phones) > 0:
        async with httpx.AsyncClient() as client:
            customers_info = await _retrive_phones_api_call(client, phones)
            if customers_info.status_code == 200:
                valid_customers = await _check_customers_validity(customers_info.json(), phones)
                await update_records_checked_flag(valid_customers)
            else:
                logger.info(customers_info, "API_CALL_FAILED", "check_newst_records")
    logger.info("", "CHECK_RECORDS_SCHEDULER_FINISHED", "check_newst_records")


async def update_customer_service_scheduler():
    logger.info("", "UPDATE_CUSTOMER_SCHEDULER_STARTED", "update_customer_service")
    active_records_phones = await retrive_activated_records(BATCH_SIZE)
    if len(active_records_phones) > 0:
        async with httpx.AsyncClient() as client:
            activated_count = await _retrive_active_codes_count_api_call(client)
            if activated_count.status_code == 200:
                records = await _update_customer(activated_count, active_records_phones, client)
                await soft_delete_records(records)
            else:
                logger.info(activated_count, "API_CALL_FAILED", "update_customer_service")
    logger.info("", "UPDATE_CUSTOMER_SCHEDULER_FINISHED", "update_customer_service")


async def _update_customer(activated_count, active_records_phones, client):
    logger.info("", "UPDATE_CUSTOMER_CHARGE_CODES_STARTED", "_update_customer_service")
    _activated_count = activated_count.json()["data"]["count"]
    if _activated_count + len(active_records_phones) < LIMIT:
        body = active_records_phones
    else:
        body = active_records_phones[: LIMIT - _activated_count]

    await _active_api_call(client, body)
    logger.info(body, "UPDATE_CUSTOMER_CHARGE_CODES_FINISHED", "_update_customer_service")
    return [f"{_body}__{CODE}" for _body in body]


async def _retrive_phones_api_call(client, phones: list):
    return await client.post(f"{CUSTOMER_SERVICE}/bulk/phones", json=phones, headers=HEADERS)


async def _retrive_active_codes_count_api_call(client):
    res = await client.get(f"{CUSTOMER_SERVICE}/{CODE}/count", headers=HEADERS)
    logger.info(
        res.json(), "RESPONSE_OF_ACTIVATED_CUSTOMER_COUNT", "_retrive_active_codes_count_api_call"
    )
    return res


async def _active_api_call(client, body):
    if len(body) > 0:
        res = await client.put(
            f"{CUSTOMER_SERVICE}/bulk/activate-code/{CODE}", json=body, headers=HEADERS
        )
        return res


async def _check_customers_validity(body: dict, phones: list) -> dict:
    logger.info(body, "CHECK_CUSTOMER_CHARGE_CODES_STARTED", "check_customers_validity")
    valid_customers: dict = body["data"]
    for phone in phones:
        new_key = f"{phone}__{CODE}"
        if valid_customers.get(phone, None) == None:
            valid_customers[new_key] = False
        elif valid_customers[phone] == CODE:
            valid_customers.pop(phone)
            valid_customers[new_key] = False
        elif valid_customers[phone] == "":
            valid_customers.pop(phone)
            valid_customers[new_key] = True
    logger.info(valid_customers, "CHECK_CUSTOMER_CHARGE_CODES_FINISHED", "check_customers_validity")
    return valid_customers
