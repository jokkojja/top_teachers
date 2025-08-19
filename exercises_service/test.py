import asyncio
from aiokafka import AIOKafkaConsumer


async def consume():
    consumer = AIOKafkaConsumer(
        "data_replication.exercises",
        bootstrap_servers="localhost:9092",
        group_id=None,  # None чтобы читать независимо от групп
        auto_offset_reset="earliest",  # читать с начала топика
        enable_auto_commit=False,
    )

    # Запуск consumer
    await consumer.start()
    try:
        async for msg in consumer:
            print(
                f"Topic: {msg.topic}, Partition: {msg.partition}, Offset: {msg.offset}"
            )
            print(f"Key: {msg.key}, Value: {msg.value.decode()}")
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume())
