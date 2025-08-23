import asyncio
import json

from loguru import logger

from app_globals import AppGlobals


async def consume_events(globals: AppGlobals):
    consumer = globals.kafka_controllers.consumer._consumer
    try:
        async for message in consumer:
            try:
                event = json.loads(message.value)
                event_type = event.get("event_type")
                if event_type == "ExerciseCreated":
                    await handle_exercise_created(globals, event)
                elif event_type == "ExerciseUpdated":
                    await handle_exercise_updated(globals, event)
                elif event_type == "ExerciseAssigned":
                    await handle_exercise_assigned(globals, event)
                else:
                    logger.error(f"Unknown event type: {event_type}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except asyncio.CancelledError:
        logger.info("Kafka consumer task cancelled")
    finally:
        await consumer.stop()


async def handle_exercise_created(globals: AppGlobals, event: dict):
    loop = asyncio.get_running_loop()
    exercise_uuid = event["payload"]["exercise_uuid"]
    exercise_title = event["payload"]["exercise_title"]
    exercise_text = event["payload"]["exercise_text"]
    await loop.run_in_executor(
        None,
        globals.postgre_controllers.exercise_controller.create_exercise,
        exercise_uuid,
        exercise_title,
        exercise_text,
    )

    logger.info(f"Consumer created exercise {exercise_uuid}")


async def handle_exercise_updated(globals: AppGlobals, event: dict):
    loop = asyncio.get_running_loop()
    exercise_uuid = event["payload"]["exercise_uuid"]
    exercise_text = event["payload"]["exercise_text"]
    await loop.run_in_executor(
        None,
        globals.postgre_controllers.exercise_controller.update_exercise,
        exercise_uuid,
        exercise_text,
    )

    logger.info(f"Consumer updated exercise {exercise_uuid}")


async def handle_exercise_assigned(globals: AppGlobals, event: dict):
    loop = asyncio.get_running_loop()
    exercise_uuid = event["payload"]["exercise_uuid"]
    candidate_uuid = event["payload"]["candidate_uuid"]
    await loop.run_in_executor(
        None,
        globals.postgre_controllers.exercise_controller.assign_exercise,
        candidate_uuid,
        exercise_uuid,
    )

    logger.info(f"Consumer assigned exercise {exercise_uuid} to {candidate_uuid}")
