from src.storage.rabbit import channel_pool
import aio_pika
import msgpack
from consumer.handlers.event_distribution import handle_event_distribution

async def main() -> None:
    queue_name = 'user_messages'
    async with channel_pool.acquire() as channel: # type: aio_pika.Channel
        await channel.set_qos(prefetch_count=1)

        queue = await channel.declare_queue(queue_name, durable=True)


        async with queue.iterator() as queue_iter:
            async for message in queue_iter: # type: aio_pika.Message
                async with message.process():
                    body = msgpack.unpackb(message.body)
                    await handle_event_distribution(body)