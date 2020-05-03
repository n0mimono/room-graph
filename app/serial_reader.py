from typing import Optional, List, Callable, Dict
import serial

import asyncio

from app.core.worker import Worker
from app.core.pubsub import Publisher


class SerialState:
    pass


class SerialParser:
    def parse(self, line: str) -> SerialState:
        return SerialState()


class SerialReader(Worker):
    def __init__(self, parser: SerialParser, key: str):
        self.interval = 1.0
        self.on_reads: List[Callable] = []
        self.parser = parser
        self.key = key

        self.ser = serial.Serial(
            port='/dev/cu.usbmodem145101',
            baudrate=9600
        )
        self.ser.setDTR(False)

    async def run(self, pubs: Dict[str, Publisher]):
        async def read_serial():
            buffer: bytes = self.ser.read_until()
            line = buffer.decode('utf-8')
            state = self.parser.parse(line)
            return state

        while True:
            await asyncio.sleep(self.interval)
            state = await read_serial()
            await pubs[self.key].publish(state)

    def close(self):
        if self.ser is not None:
            self.ser.close()


class SerialReaderDummy(Worker):
    def __init__(self, parser: SerialParser, key: str):
        self.interval = 1.0
        self.on_reads: List[Callable] = []
        self.parser = parser
        self.key = key

        self.line = '27.0, 21.0'

    async def run(self, pubs: Dict[str, Publisher]):
        async def read_serial():
            line = self.line
            state = self.parser.parse(line)
            return state

        while True:
            await asyncio.sleep(self.interval)
            state = await read_serial()
            await pubs[self.key].publish(state)

    def close(self):
        pass
