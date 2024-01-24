from beanie import Document
from models import Charge, object_mapper
from beanie.operators import In
from schema import CodeActivationResult
from common import MyLogger


logger = MyLogger()

charge_collection: Document = Charge


async def add_record(new_charge_record) -> Charge:
    _chargge = Charge(
        **new_charge_record, checked_label=False, working_label=False, activated_label=False
    )
    customer = await _chargge.create()
    return customer


async def retrive_record(limit: int) -> Charge:
    _records = []

    async for record in charge_collection.find(
        Charge.checked_label == False and Charge.working_label == False
    ).sort(Charge.timestamp).limit(limit):
        record.working_label = True
        _records.append(object_mapper(record))
        await record.save()
    return _records


async def retrive_records_phone(limit: int) -> list:
    logger.info("", "RETRIVED_NEWST_RECORDS_STARTED", "retrive_records_phone")
    _records = []
    async for record in charge_collection.find(
        Charge.checked_label == False and Charge.working_label == False
    ).sort(Charge.timestamp).limit(limit):
        record.working_label = True
        _records.append(record.phone_number_code.split("__")[0])
        await record.save()
    logger.info(_records, "RETRIVED_NEWST_RECORDS_FINISHED", "retrive_records_phone")
    return _records


async def retrive_activated_records(limit: int) -> list:
    logger.info("", "RETRIVED_ACTIVE_RECORDS_STARTED", "retrive_activated_records")
    _records = []

    async for record in charge_collection.find(Charge.activated_label == True).sort(
        Charge.timestamp
    ).limit(limit):
        record.working_label = True
        _records.append(record.phone_number_code.split("__")[0])
        await record.save()
    logger.info(_records, "RETRIVED_ACTIVE_RECORDS_FINISHED", "retrive_activated_records")
    return _records


async def update_records_checked_flag(custmers_info: dict) -> None:
    l = [customer for customer in custmers_info.keys()]
    async for record in charge_collection.find(In(Charge.phone_number_code, l)):
        record.activated_label = custmers_info[record.phone_number_code]
        record.checked_label = True
        await record.save()
    return {"updated": len(custmers_info)}


async def soft_delete_records(phone_codes) -> None:
    logger.info("", "SOFT_DELETE_RECORDS_STARTED", "soft_delete_records")

    async for record in charge_collection.find(In(Charge.phone_number_code, phone_codes)):
        record.activated_label = False
        await record.save()
    logger.info(
        {"deleted": len(phone_codes)}, "SOFT_DELETE_RECORDS_FINISHED", "soft_delete_records"
    )
