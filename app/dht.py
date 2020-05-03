import time

from app.serial_reader import SerialState, SerialParser


class DhtState(SerialState):
    def __init__(self, humidity: float, temperature: float, ts: int, ok: bool):
        self.humidity = humidity
        self.temperature = temperature
        self.ts = ts
        self.ok = ok

    def to_json(self) -> str:
        return {
            'h': self.humidity,
            't': self.temperature,
            'ts': self.ts,
            'ok': self.ok
        }

    @classmethod
    def from_json(cls, payload):
        return cls(
            humidity=payload['h'],
            temperature=payload['t'],
            ts=int(payload['ts']),
            ok=bool(payload['ok'])
        )


class DhtParser(SerialParser):
    def parse(self, line: str) -> SerialState:
        args = line.split(sep=',')
        if len(args) > 1:
            return DhtState(
                humidity=float(args[0]),
                temperature=float(args[1]),
                ts=int(time.time()),
                ok=True
            )
        else:
            return DhtState(
                humidity=-1,
                temperature=-1,
                ts=int(time.time()),
                ok=False
            )
