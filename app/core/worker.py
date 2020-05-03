from typing import Optional, List, Callable, Any, Dict
import asyncio

from app.core.pubsub import PubSub, Publisher, Subscriber


class Worker:
    def __init__(self):
        pass

    async def run(self, pubs: Dict[str, Publisher]):
        pass

    def close(self):
        pass


class WorkerController:
    def __init__(self):
        self.workers: List[Worker] = []
        self.pubsub = PubSub()

        self.loop = asyncio.get_event_loop()

    def add(self, worker: Worker):
        self.workers.append(worker)

    def run(self):
        async def _run_workers():
            tasks = [worker.run(self.pubsub.publishers)
                     for worker in self.workers]
            await asyncio.gather(*tasks, loop=self.loop)

        self.loop.run_until_complete(_run_workers())

    def close(self):
        for worker in self.workers:
            worker.close()
        self.loop.close()
