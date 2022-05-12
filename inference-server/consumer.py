import asyncio
import nats
from nats.errors import TimeoutError
import pickle
import traceback


class BatchPullConsumer:
    def __init__(
            self,
            batchSize: int,
            errorLogger: object,
    ):
        self.batchSize = batchSize
        self.errorLogger = errorLogger
        self.client = None
        self.jetstream = None
        self.sub = None
        self.mongoClient = None
        self.subjectName = None

    async def connect(
            self,
            host: str,
            durable: str,
            stream: str,
            subject: list,
    ):
        try:
            self.client = await nats.connect(host)
            self.jetstream = self.client.jetstream()
            self.sub = await self.jetstream.pull_subscribe(subject[0], durable, stream)
            self.subjectName = subject[0]
            print(await self.sub.consumer_info())
        except TimeoutError:
            return False

    async def read(self):
        try:
            pulled = await self.sub.fetch(self.batchSize, 5.0)
            batch = [pickle.loads(message.data) for message in pulled]

            # asynchronous ack to the Nats server
            for message in pulled:
                await message.ack()
            await asyncio.sleep(1)
        except TimeoutError:
            pass
        except:
            print(traceback.format_exc())
