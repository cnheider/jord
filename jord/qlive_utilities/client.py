from enum import Enum
from functools import partial
from typing import Any, Callable

import zmq
from warg import AlsoDecorator

__all__ = ["QliveClient"]

from jord.qlive_utilities import QliveRPCMethodEnum, build_package, QliveRPCMethodMap

import inspect


class DisSatisfactionEnum(Enum):
    none = "none"
    args = "args"
    kws = "kws"
    argskws = "argskws"


def partial_satisfied(partial_fn: Callable) -> bool:
    signature = inspect.signature(partial_fn.func)
    try:
        signature.bind(*partial_fn.args, **partial_fn.keywords)
        return True
    except TypeError:
        return False


class QliveClient(AlsoDecorator):
    """
    Client for sending data to qgis instance
    """

    def __init__(self, addr: str = "tcp://localhost:5555"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.addr = addr

        for method in QliveRPCMethodEnum:
            actual_callable = QliveRPCMethodMap[method]

            if False:
                partial_build_package = partial(build_package, method.value)
                if False and partial_satisfied(
                    partial_build_package
                ):  # TODO: RESOLVE PARTIAL APPLICATION SATISFACTION.

                    def a():
                        self.send(partial_build_package())

                    rpc_method = a
                elif True:

                    def a(*args):
                        self.send(partial_build_package(*args))

                    rpc_method = a
                elif False:

                    def a(**kwargs):
                        self.send(partial_build_package(**kwargs))

                    rpc_method = a
                elif False:

                    def a(*args, **kwargs):
                        self.send(partial_build_package(*args, **kwargs))

                    rpc_method = a
                else:
                    raise NotImplementedError
            elif False:
                rpc_method = lambda *args: self.send(
                    partial(build_package, method)(*args)
                )
            elif False:
                rpc_method = lambda *args: self.send(build_package(method, *args))
            else:

                def a(*args):
                    return self.send(build_package(method, *args))

                rpc_method = a

            rpc_method.__doc__ = actual_callable.__doc__
            print(method.value, rpc_method)
            setattr(self, method.value, rpc_method)

    def __enter__(self):
        self.socket.connect(self.addr)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.socket.close()

    def send(self, *args) -> Any:
        self.socket.send(*args)
        return self.socket.recv()


if __name__ == "__main__":
    # QliveClient().clear_all()
    # QliveClient().remove_layers()
    # print(QliveClient().clear_all.__doc__)
    # print(QliveClient().__dict__)
    def uahdsuh():
        with QliveClient() as qlive:
            print("calling", qlive.add_wkts)
            qlive.add_wkts({"a": "POINT (-66.86 10.48)"})

    # QliveClient().add_dataframe(None)

    uahdsuh()
