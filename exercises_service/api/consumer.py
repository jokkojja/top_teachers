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

                if event_type == "CandidateCreated":
                    await handle_hiring_candidate(globals, event)
                else:
                    logger.error(f"Unknown event type: {event_type}")
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    except asyncio.CancelledError:
        logger.info("Kafka consumer task cancelled")
    finally:
        await consumer.stop()


async def handle_hiring_candidate(globals: AppGlobals, event: dict):
    loop = asyncio.get_running_loop()
    candidate_uuid = event["payload"]["candidate_uuid"]
    candidate_name = event["payload"]["candidate_name"]
    await loop.run_in_executor(
        None,
        globals.postgre_controllers.candidate_controller.create_candidate,
        candidate_uuid,
        candidate_name,
    )

    logger.info(f"""Consumer created candidate {candidate_uuid} {candidate_name}""")
