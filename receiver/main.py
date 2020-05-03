import json
import os

from google.cloud import pubsub
import requests


class Env:
    def __init__(self):
        self.path = os.environ['GCP_PUBSUB_SUBSCRIPTION_PATH']
        self.influxdb_url = os.environ['INFLUXDB_URL']
        self.influxdb_db = os.environ['INFLUXDB_DB']


class Emitter:
    def __init__(self, url, db):
        self.url = url
        self.db = db

    def receive(self, data: bytes):
        try:
            url = os.path.join(self.url, f'write?db={self.db}')

            state = json.loads(data.decode())
            t = state['t']
            h = state['h']
            ts = state['ts']
            ok = state['ok']
            payload = f'dht,ok={ok} t={t},h={h},ts={ts}'

            requests.post(
                url=url,
                data=payload.encode()
            )
        except Exception as e:
            print(e)


if __name__ == "__main__":
    env = Env()

    subscriber = pubsub.SubscriberClient()
    emitter = Emitter(env.influxdb_url, env.influxdb_db)

    def callback(message):
        data: bytes = message.data
        emitter.receive(data)
        message.ack()

    future = subscriber.subscribe(env.path, callback)
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
