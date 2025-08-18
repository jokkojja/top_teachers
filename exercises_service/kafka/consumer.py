import asyncio
import json
from typing import Callable

from aiokafka import AIOKafkaConsumer

from kafka.config import KafkaConsumerConfig


class KafkaConsumerService:
    def __init__(
        self, config: KafkaConsumerConfig, topics: list[str], handler: Callable
    ):
        self._topics = topics
        self._handler = handler
        self._consumer = AIOKafkaConsumer(
            *self._topics,
            bootstrap_servers=config.bootstrap,
            group_id=config.group_id,
            auto_offset_reset=config.auto_offset_reset,
            enable_auto_commit=True,
        )

    async def start(self):
        await self._consumer.start()
        asyncio.create_task(self._consume())

    async def stop(self):
        if self._consumer:
            await self._consumer.stop()

    async def _consume(self):
        async for msg in self._consumer:
            value = json.loads(msg.value.decode())
            await self._handler(msg.topic, value)
