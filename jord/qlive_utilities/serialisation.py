import base64
import json
from typing import Tuple, Sequence


__all__ = ["build_package", "read_package"]


from jord.qlive_utilities.procedures import QliveRPCMethodEnum, QliveRPCMethodMap


def build_package(method: QliveRPCMethodEnum, *args: str) -> bytes:
    d = {"method": method.value, "args": list(args)}
    message = str(d)
    ascii_message = message.encode("ascii")
    output_byte = base64.b64encode(ascii_message)
    return output_byte


def read_package(package: bytes) -> Tuple[QliveRPCMethodEnum, Sequence[str]]:
    msg_bytes = base64.b64decode(package)
    ascii_msg = msg_bytes.decode("ascii")
    ascii_msg = ascii_msg.replace(
        "'", '"'
    )  # Json library convert string dictionary to real dictionary type. Double quotes is standard format for json
    print(ascii_msg)
    res = json.loads(ascii_msg)  # convert string dictionary to dict format
    method = QliveRPCMethodMap[QliveRPCMethodEnum(res["method"])]
    args = res["args"]
    return method, args


if __name__ == "__main__":
    print(read_package(build_package(method=QliveRPCMethodEnum.clear_all)))
