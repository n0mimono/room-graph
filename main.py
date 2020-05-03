from typing import Any, Dict, Optional
from datetime import datetime
import json
import os

import requests
from google.cloud import pubsub

from app.util import Util
from app.core.worker import WorkerController, Worker
from app.core.pubsub import Subscriber, Publisher
from app.serial_reader import SerialReaderDummy, SerialReader
from app.dht import DhtState, DhtParser


class WorkerExample(Worker):
    async def run(self, pubs: Dict[str, Publisher]):
        print('Hello, world!')


class SubscriberExample(Subscriber):
    async def subscribe(self, value: Any):
        print(value)


class Printer(Subscriber):
    def __init__(self, key: str):
        super().__init__(key)

    async def subscribe(self, value: Any):
        state: DhtState = value

        print(state.to_json())


class WebApiClient(Subscriber):
    def __init__(self, key: str):
        super().__init__(key)
        self.url: Optional[str] = None

    async def subscribe(self, value: Any):
        state: DhtState = value

        if self.url is not None:
            requests.post(
                url=self.url,
                json={
                    'payload': state.to_json(),
                    'hash': Util.get_sig(json.dumps(state.to_json()))
                }
            )


class GcpPubSubPublisher(Subscriber):
    def __init__(self, key: str):
        super().__init__(key)
        publisher = pubsub.PublisherClient()

        self.publisher = publisher
        self.topic: Optional[str] = None

    async def subscribe(self, value: Any):
        state: DhtState = value
        now = datetime.now().strftime('%Y-%m-%dT%H:%M:%S-00:00')

        if self.topic != None:
            self.publisher.publish(
                topic=self.topic,
                data=json.dumps(state.to_json()).encode(),
                EventTimeStamp=now
            )


if __name__ == "__main__":
    wc = WorkerController()

    topic_key = 'dht'

    worker_example = WorkerExample()
    #serial_reader = SerialReaderDummy(parser=DhtParser(), key=topic_key)
    serial_reader = SerialReader(parser=DhtParser(), key=topic_key)
    serial_reader.interval = 3

    wc.add(worker_example)
    wc.add(serial_reader)

    subscriber_example = SubscriberExample(key=topic_key)
    gcp_pubsub = GcpPubSubPublisher(key=topic_key)
    printer = Printer(key=topic_key)

    #gcp_pubsub.topic = 'projects/project/topics/topic'
    if 'GCP_PUBSUB_ROOM_GRAPH_TOPIC' in os.environ:
        gcp_pubsub.topic = os.environ['GCP_PUBSUB_ROOM_GRAPH_TOPIC']

    wc.pubsub.add_publisher(key=topic_key)
    wc.pubsub.add_subscriber(subscriber=subscriber_example)
    wc.pubsub.add_subscriber(subscriber=printer)
    wc.pubsub.add_subscriber(subscriber=gcp_pubsub)

    try:
        wc.run()
    except KeyboardInterrupt:
        wc.close()
