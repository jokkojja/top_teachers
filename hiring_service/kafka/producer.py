import json
from typing import Self, TypeAlias

from aiokafka import AIOKafkaProducer
from tenacity import retry, stop_after_attempt, wait_fixed


from kafka.config import KafkaProducerConfig

Event: TypeAlias = dict[str, str]


class KafkaProducerService:
    @retry(stop=stop_after_attempt(10), wait=wait_fixed(5))
    def __init__(self, config: KafkaProducerConfig):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=config.bootstrap,
            acks=config.acks,
            linger_ms=config.linger_ms,
        )

    @classmethod
    def from_env(cls) -> Self:
        config = KafkaProducerConfig.from_env()
        return cls(config)

    async def start(self):
        await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()

    async def send(self, topic: str, event: Event):
        if not self._producer:
            raise RuntimeError("Producer not started")

        await self._producer.send_and_wait(topic, json.dumps(event).encode("utf-8"))
