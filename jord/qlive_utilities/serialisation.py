import base64
import json
import pickle
from typing import Tuple, Sequence

__all__ = ["build_package", "read_package"]

from jord.qlive_utilities.procedures import QliveRPCMethodEnum, QliveRPCMethodMap


def build_package(method: QliveRPCMethodEnum, *args) -> bytes:
    return pickle.dumps({"method": method.value, "args": args})
    # return json.dump({"method": method.value, "args": args})
    # return base64.b64encode(str({"method": method.value, "args": args}).encode("ascii"))


def read_package(package: bytes) -> Tuple[QliveRPCMethodEnum, Sequence[str]]:
    if False:
        str_dict = (
            base64.b64decode(package)
            .decode("ascii")
            .replace(
                # Json library convert string dictionary to real dictionary type. Double quotes is standard format for json
                "'",
                '"',
            )
        )
        print(str_dict)
        res_dict = json.loads(str_dict)  # convert string dictionary to dict format
    else:
        res_dict = pickle.loads(package)
    return QliveRPCMethodMap[QliveRPCMethodEnum(res_dict["method"])], res_dict["args"]


if __name__ == "__main__":
    print(read_package(build_package(method=QliveRPCMethodEnum.clear_all)))
