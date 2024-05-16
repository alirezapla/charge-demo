import asyncio
import json

import orjson
from aio_pika import connect_robust
from aio_pika.abc import AbstractIncomingMessage, AbstractRobustConnection
from decouple import config
from schema import DispatcherMessage

from common import MyLogger, publish

from .charge import add_record

logger = MyLogger()
END_QUEUE = "matching-result"
rabbit_user = config("rabbitmq_username", "guest")
rabbit_pass = config("rabbitmq_password", "guest")
rabbit_host = config("rabbitmq_addresses", "rabbitmq:5672")
rabbit_vhost = config("rabbitmq_virtual_host", "pla")
BROKER = f"amqp://{rabbit_user}:{rabbit_pass}@{rabbit_host}/{rabbit_vhost}"


async def con() -> None:
    while True:
        try:
            conn = await connect_robust(BROKER)
            async with conn:
                logger.info(">>> Consuming charge service  >>>", "CONSUMING_STARTED", "con")
                queue = await broker_ready_up(conn, "dispatcher")
                async with queue.iterator() as queue_iter:
                    async for message in queue_iter:
                        async with message.process():
                            await message_handler(message, "next")
        except ConnectionError as e:
            await asyncio.sleep(5)


async def broker_ready_up(conn: AbstractRobustConnection, listen_queue: str):
    channel = await conn.channel()
    await channel.set_qos(prefetch_count=1)
    queue = await channel.declare_queue(listen_queue, passive=True, durable=True)
    return queue


async def message_handler(message: AbstractIncomingMessage, send_queue: str):
    body = _fetch_message(message)
    await add_record(orjson.loads(message.body.decode("utf8")))
    logger.info(body, "REQUEST_INSERTED", "message_handler")


def _fetch_message(message: AbstractIncomingMessage) -> DispatcherMessage:
    _msg = DispatcherMessage(**orjson.loads(message.body.decode("utf8")))
    return _msg


def _result_message(message: DispatcherMessage) -> dict:
    return json.dumps({
        "transaction_id": message.transaction_id,
        "phone_number_code": message.phone_number_code,
        "timestamp": message.timestamp,
    })


async def _error_exception(transaction_id: str, message: str = "", module: str = None):
    err = _error_message(transaction_id)
    await publish(END_QUEUE, BROKER, err)
    logger.error(
        f"{module}--{message}",
        "DEMO_ERROR_EXCEPTION",
        "_error_exception",
    )


def _error_message(transaction_id: str):
    res = {"transaction_id": transaction_id, "error": "true"}
    return json.dumps(res)


def loop():
    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    loop.create_task(con())


if __name__ == "__main__":
    loop()
