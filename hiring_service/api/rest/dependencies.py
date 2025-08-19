from fastapi import Depends, FastAPI

from api.rest.app import app
from app_globals import AppGlobals, PostgreControllers
from kafka.consumer import KafkaConsumerService
from kafka.producer import KafkaProducerService


def get_app() -> FastAPI:
    return app


def get_app_globals(app: FastAPI = Depends(get_app)) -> AppGlobals:
    return app.state.globals


def get_database_controllers(
    globals: AppGlobals = Depends(get_app_globals),
) -> PostgreControllers:
    return globals.postgre_controllers


def get_kafka_producer(
    globals: AppGlobals = Depends(get_app_globals),
) -> KafkaProducerService:
    return globals.kafka_controllers.producer


def get_kafka_consumer(
    globals: AppGlobals = Depends(get_app_globals),
) -> KafkaConsumerService:
    return globals.kafka_controllers.consumer
