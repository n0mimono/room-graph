from typing import Optional, List, Callable, Any, Dict
import asyncio


class Publisher:
    def __init__(self, key: str, pubsub: Any):
        self.key = key
        self._pubsub = pubsub

    async def publish(self, value: Any):
        await self._pubsub.publish(self.key, value)


class Subscriber:
    def __init__(self, key: str):
        self.key = key

    async def subscribe(self, value: Any):
        pass


class PubSub:
    def __init__(self):
        self.publishers: Dict[str, Publisher] = {}
        self.subscribers: List[Subscriber] = []
        self.on_error = lambda e: print(e)

    async def publish(self, key: str, value: Any):
        for subscriber in self.subscribers:
            if subscriber.key == key:
                try:
                    await subscriber.subscribe(value)
                except Exception as e:
                    self.on_error(e)

    def add_publisher(self, key: str):
        self.publishers[key] = Publisher(key, self)

    def add_subscriber(self, subscriber: Subscriber):
        self.subscribers.append(subscriber)
