from email import message
from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from schema import ChargeCodeRequest
from common import publish, create_connection, publish_with_connection
from datetime import datetime
import uuid
import uvicorn
from decouple import config
import json
from aio_pika import connect_robust, Connection
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.status import HTTP_429_TOO_MANY_REQUESTS
from typing import Callable, Awaitable, Any
from limiter import hit

api = FastAPI(title="Distpacher", version="0.0.1")

rabbit_user = config("rabbitmq_username", "guest")
rabbit_pass = config("rabbitmq_password", "guest")
rabbit_host = config("rabbitmq_addresses", "localhost:5672")
rabbit_vhost = config("rabbitmq_virtual_host", "pla")
BROKER = f"amqp://{rabbit_user}:{rabbit_pass}@{rabbit_host}/{rabbit_vhost}"


async def rate_provider(request: Request) -> str:
    return 3


async def identifier(request: Request) -> str:
    ip = request.client.host
    return ip


async def _default_callback(request: Request):
    raise HTTPException(status_code=HTTP_429_TOO_MANY_REQUESTS, detail="request limit reached")


class RateLimitMiddleware:
    def __init__(
        self,
        rate_provider: Callable[[Request], Awaitable[int]] = rate_provider,
        identifier: Callable[[Request], Awaitable[str]] = identifier,
        callback: Callable[[Request], Awaitable[Any]] = _default_callback,
    ):
        self.identifier = identifier
        self.callback = callback
        self.rate_provider = rate_provider

    async def __call__(self, request: Request):
        callback = self.callback
        identifier = self.identifier
        rate_provider = self.rate_provider

        key = await identifier(request)
        rate = await rate_provider(request)

        if not hit(key=key, rate_per_minute=rate):
            return await callback(request)


async def live_connection():
    return await create_connection(BROKER)


class RabbitMQManager:
    def __init__(self) -> None:
        self.amqp_dsn = BROKER
        self.connection = None

    async def get_connection(self) -> Connection:
        if self.connection is None or self.connection.is_closed:
            self.connection = await connect_robust(self.amqp_dsn)
        return self.connection


async def get_rabbitmq_connection(
    rabbitmq_manager: RabbitMQManager = Depends(RabbitMQManager),
):
    return await rabbitmq_manager.get_connection()


rate_limit = RateLimitMiddleware(rate_provider=rate_provider)


@api.post("/submit_code/")
async def submit_code(
    request: ChargeCodeRequest,
    connection=Depends(get_rabbitmq_connection),
    dependencies=Depends(RateLimitMiddleware()),
):
    message = {
        "phone_number_code": f"{request.phone_number}__{request.charge_code}",
        "transaction_id": str(uuid.uuid4()),
        "timestamp": datetime.now().timestamp(),
    }
    print(connection)
    # await publish("dispatcher", BROKER, json.dumps(message))
    await publish_with_connection(connection, "dispatcher", json.dumps(message))
    return JSONResponse({"response": message["transaction_id"]})


if __name__ == "__main__":
    uvicorn.run("app:api", host="0.0.0.0", port=5001, reload=True, log_level="debug")
