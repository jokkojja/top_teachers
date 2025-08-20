from typing import Self

from aiokafka import AIOKafkaConsumer

from kafka.config import KafkaConsumerConfig


class KafkaConsumerService:
    def __init__(self, config: KafkaConsumerConfig):
        self._consumer = AIOKafkaConsumer(
            *config.topics,
            bootstrap_servers=config.bootstrap,
            group_id=config.group_id,
            auto_offset_reset=config.auto_offset_reset,
            enable_auto_commit=True,
        )

    @classmethod
    def from_env(cls) -> Self:
        config = KafkaConsumerConfig.from_env()
        return cls(config)

    async def start(self):
        await self._consumer.start()

    async def stop(self):
        if self._consumer:
            await self._consumer.stop()
