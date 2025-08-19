from dataclasses import dataclass
from typing import Self

from kafka.consumer import KafkaConsumerService
from kafka.producer import KafkaProducerService
from repos.postgre import (
    PostgreExercisesController,
    PostgreUserContoller,
    PostgreCandidateController,
)


@dataclass(frozen=True)
class PostgreControllers:
    users_controller: PostgreUserContoller
    exercises_controller: PostgreExercisesController
    candidate_controller: PostgreCandidateController

    @classmethod
    def from_env(cls) -> Self:
        users_controller = PostgreUserContoller.from_env()
        exercises_controller = PostgreExercisesController.from_env()
        candidate_controller = PostgreCandidateController.from_env()
        return cls(users_controller, exercises_controller, candidate_controller)


@dataclass(frozen=True)
class KafkaControllers:
    producer: KafkaProducerService
    consumer: KafkaConsumerService

    @classmethod
    def from_env(cls) -> Self:
        producer = KafkaProducerService.from_env()
        consumer = KafkaConsumerService.from_env()

        return cls(producer, consumer)

    async def start(self) -> None:
        await self.producer.start()
        await self.consumer.start()

    async def shutdown(self) -> None:
        await self.producer.stop()
        await self.consumer.stop()


@dataclass(frozen=True)
class AppGlobals:
    postgre_controllers: PostgreControllers
    kafka_controllers: KafkaControllers

    @classmethod
    async def create(cls) -> Self:
        database_session = PostgreControllers.from_env()
        kafka_controllers = KafkaControllers.from_env()

        await kafka_controllers.start()

        return cls(database_session, kafka_controllers)

    async def shutdown(self) -> None:
        await self.kafka_controllers.shutdown()
