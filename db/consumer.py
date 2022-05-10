"""
Batch Pull Consumer
"""

import asyncio
import nats
from nats.errors import TimeoutError
import pickle
import sys
from logger import Logger


LOG = Logger('$path')
HOST = '192.168.1.101:30042'
PODNAME = 'psub-1'


async def connect(
        host: str,
        subject: str,
        durable: str,
        stream: str,
        subjects: list,
):
    try:
        client = await nats.connect(host)
        jetstream = client.jetstream()
        # await jetstream.delete_stream('data')
        streamInfo = await jetstream.add_stream(name=stream, subjects=subjects)
        print(streamInfo)
        sub = await jetstream.pull_subscribe(subject, durable, stream)
        return sub
    except TimeoutError:
        return False


async def main():
    sub = await connect(HOST, 'scraped', PODNAME, 'data', ['scraped'])
    if sub is False:
        print('cannot connect to the Nats server')
        sys.exit(1)

    while True:
        try:
            batch = await sub.fetch(10, 5.0)
            for i in batch:
                print(pickle.loads(i.data))
                await i.ack()
        except TimeoutError:
            pass


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
