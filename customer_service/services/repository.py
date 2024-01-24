from typing import List, Union
from beanie import PydanticObjectId, Document
from models.customer import Customer, object_mapper
from models.transactions import Transaction
from schemas.customer import CreateCustomerModel, AddTransactionCustomerModel
from schemas.transaction import CreateTransaction
from exceptions.customer_exceptions import BadRequest
from beanie.operators import In

customer_collection: Document = Customer


async def retrieve_customers(limit_number: int) -> List[Customer]:
    customers = await customer_collection.find().limit(limit_number).to_list()
    _customers = []
    for customer in customers:
        _customers.append(object_mapper(customer))
    return _customers


async def add_customer(new_customer: CreateCustomerModel) -> Customer:
    _customer = Customer(**new_customer.dict(), transactions=[])
    customer = await _customer.create()
    return customer


async def retrieve_customer(id: PydanticObjectId) -> Customer:
    customer = await customer_collection.get(id)
    if customer:
        return object_mapper(customer)
    return None


async def retrieve_customer_by_phone(phone_number: str) -> Customer:
    customer = await customer_collection.find_one(Customer.phone_number == phone_number)
    print(customer)
    if customer:
        return object_mapper(customer)
    return None


async def retrieve_group_customers(phone_numbers: list[str]) -> dict:
    customers = await customer_collection.find(In(Customer.phone_number, phone_numbers)).to_list()
    _counstmers = dict()
    for customer in customers:
        _counstmers[customer.phone_number] = customer.charge_code
    return _counstmers


async def update_group_customers(phone_numbers: list[str], code) -> dict:
    _updated_count = 0
    async for customer in customer_collection.find(In(Customer.phone_number, phone_numbers)):
        customer.charge_code = code
        await customer.save()
        _updated_count += 1
    return {"updated": _updated_count}


async def retrieve_customer_balance(id: PydanticObjectId) -> Customer:
    customer: Customer = await customer_collection.get(id)
    if customer:
        return {"balance": await get_balance(customer)}


async def retrieve_activated_code_count(code: str) -> Customer:
    customer: Customer = await customer_collection.find(Customer.charge_code == code).to_list()
    return {"count": len(customer)}


async def delete_customer(id: PydanticObjectId) -> bool:
    customer = await customer_collection.get(id)
    if customer:
        await customer.delete()
        return True


async def update_customer_data(id: PydanticObjectId, data: dict) -> Union[bool, Customer]:
    des_body = {k: v for k, v in data.items() if v is not None}
    update_query = {"$set": {field: value for field, value in des_body.items()}}
    await customer_collection.find_one(customer_collection.id == id).update(update_query)

    return {"status": "Updated"}


async def add_transaction_to_customer_transactions(
    id: PydanticObjectId, req: AddTransactionCustomerModel
) -> Union[bool, Customer]:
    customer: Customer = await customer_collection.get(id)
    if customer:
        balance = await get_balance(customer)
        for transaction in req.transactions:
            if (balance < 0 and transaction.amount > 0) or balance > 0:
                customer.transactions.append(await create_transacion(transaction))
            else:
                return BadRequest("Not enough credit")
        await customer.update({"$set": {"transactions": customer.transactions}})

    return {"status": "Added"}


async def create_transacion(new_transaction: CreateTransaction):
    _transaction = Transaction(**new_transaction.dict())
    transaction = await _transaction.create()
    return transaction


async def get_balance(customer: Customer):
    balance = 0
    for transaction in customer.transactions:
        balance += transaction.amount
    return balance
