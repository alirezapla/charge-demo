import asyncio
from typing import Any, Dict

from aio_pika import DeliveryMode, ExchangeType, Message, connect_robust

from .log_handler import MyLogger

SEVERITY = "info"

logger = MyLogger()


async def publish(queue_name: str, host: str, message: str) -> None:
    conn = await connect_robust(host)
    async with conn:
        channel = await conn.channel(publisher_confirms=True)
        queue = await channel.declare_queue(queue_name, passive=True)

        logger.info(f"Send message:{message}", "PUBLISHED_TO_NEXT_QUEUE", "pub")
        await channel.default_exchange.publish(
            Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=queue_name,
        )


async def publish_with_connection(conn, queue_name: str, message: str) -> None:
    async with conn:
        channel = await conn.channel(publisher_confirms=True)
        queue = await channel.declare_queue(queue_name, passive=True)

        logger.info(f"Send message:{message}", "PUBLISHED_TO_NEXT_QUEUE", "pub")
        await channel.default_exchange.publish(
            Message(body=message.encode(), delivery_mode=DeliveryMode.PERSISTENT),
            routing_key=queue_name,
        )


async def create_connection(host: str):
    conn = await connect_robust(host)
    return conn
