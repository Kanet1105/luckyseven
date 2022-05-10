import nats
from nats.errors import TimeoutError


class Publisher:
    def __init__(self, host):
        self.host = host
        self.client = None
        self.jetstream = None

    async def connect(self) -> object:
        try:
            self.client = await nats.connect(self.host)
            self.jetstream = self.client.jetstream()
        except TimeoutError:
            return False

    async def publish(
            self,
            subject: str,
            payload: bytes,
            timeout: float,
            stream: str,
            headers: dict,
    ) -> object:
        # check jetstream connection
        if self.jetstream is None:
            streamInfo = await self.connect()
            if streamInfo is False:
                return False

        # publish the message
        try:
            return await self.jetstream.publish(subject, payload, timeout, stream, headers)
        except TimeoutError:
            return False
