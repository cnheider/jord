from functools import partial
from typing import Callable
from jord.qlive_utilities import (
    QliveClient,
    QliveRPCMethodEnum,
    QliveRPCMethodMap,
    build_package,
)


__all__ = ["AutoQliveClient"]

from jord.qlive_utilities.clients.arguments import partial_satisfied


class AutoQliveClient(QliveClient):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for method in QliveRPCMethodEnum:
            actual_callable = QliveRPCMethodMap[method]

            if False:
                partial_build_package = partial(build_package, method)
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

                def wrapped(method_, *args_) -> Callable:
                    return self.send(build_package(method_, *args_))

                rpc_method = partial(wrapped, method)

            rpc_method.__doc__ = actual_callable.__doc__
            setattr(self, method.value, rpc_method)


if __name__ == "__main__":
    # QliveClient().clear_all()
    # QliveClient().remove_layers()
    # print(QliveClient().clear_all.__doc__)
    # print(QliveClient().__dict__)
    def uahdsuh():
        with AutoQliveClient() as qlive:
            qlive.add_wkts({"a": "POINT (-66.86 10.48)"})

    # QliveClient().add_dataframe(None)

    uahdsuh()
