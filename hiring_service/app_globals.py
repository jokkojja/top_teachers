from dataclasses import dataclass
from typing import Self

from kafka.consumer import KafkaConsumerService
from kafka.producer import KafkaProducerService
from repos.postgre import PostgreCandidateController, PostgreExerciseController


@dataclass(frozen=True)
class PostgreControllers:
    candidate_controller: PostgreCandidateController
    exercise_controller: PostgreExerciseController

    @classmethod
    def from_env(cls) -> Self:
        candidate_controller = PostgreCandidateController.from_env()
        exercise_controller = PostgreExerciseController.from_env()
        return cls(candidate_controller, exercise_controller)


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
