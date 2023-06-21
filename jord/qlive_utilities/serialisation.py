import base64
import json
import pickle
from enum import Enum
from typing import Tuple, Sequence

__all__ = ["build_package", "read_package"]

from sorcery import assigned_names

from jord.qlive_utilities.procedures import QliveRPCMethodEnum, QliveRPCMethodMap


class SerialisationMethodEnum(Enum):
    json, pickle = assigned_names()


SERIALISATION_METHOD = SerialisationMethodEnum.pickle


def build_package(method: QliveRPCMethodEnum, *args) -> bytes:
    """

    :param method:
    :param args:
    :return:
    """
    if SERIALISATION_METHOD == SerialisationMethodEnum.pickle:
        return pickle.dumps({"method": method.value, "args": args})
    elif SERIALISATION_METHOD == SERIALISATION_METHOD.json:
        return json.dump({"method": method.value, "args": args})  # TODO: ?
        # return base64.b64encode(str({"method": method.value, "args": args}).encode("ascii"))
    else:
        raise NotImplemented


def read_package(package: bytes) -> Tuple[QliveRPCMethodEnum, Sequence[str]]:
    """

    :param package:
    :return:
    """
    if SERIALISATION_METHOD == SerialisationMethodEnum.json:
        str_dict = (
            base64.b64decode(package)
            .decode("ascii")
            .replace(
                # Json library convert string dictionary to real dictionary type. Double quotes is standard format for json
                "'",
                '"',
            )
        )
        res_dict = json.loads(str_dict)  # convert string dictionary to dict format
    elif SERIALISATION_METHOD == SerialisationMethodEnum.pickle:
        res_dict = pickle.loads(package)
    else:
        raise NotImplemented
    return QliveRPCMethodMap[QliveRPCMethodEnum(res_dict["method"])], res_dict["args"]


if __name__ == "__main__":
    print(read_package(build_package(method=QliveRPCMethodEnum.clear_all)))
