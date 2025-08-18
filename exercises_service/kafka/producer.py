import json

from aiokafka import AIOKafkaProducer

from kafka.config import KafkaProducerConfig


class KafkaProducerService:
    def __init__(self, config: KafkaProducerConfig):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=config.bootstrap,
            acks=config.acks,
            linger_ms=config.linger_ms,
        )

    async def start(self):
        await self._producer.start()

    async def stop(self):
        if self._producer:
            await self._producer.stop()

    async def send(self, topic: str, key: str, value: dict):
        if not self._producer:
            raise RuntimeError("Producer not started")

        await self._producer.send_and_wait(
            topic,
            key=key.encode(),
            value=json.dumps(value).encode(),
        )
