from typing import Any

import zmq
from warg import AlsoDecorator


__all__ = ["QliveClient"]


class QliveClient(AlsoDecorator):
    def __init__(self, addr: str = "tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.addr = addr

    def __enter__(self):
        self.socket.connect(self.addr)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, *args) -> Any:
        self.socket.send(*args)
        return self.socket.recv()
