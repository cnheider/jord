__all__ = []

from jord.qlive_utilities.procedures import QliveRPCMethodEnum
from jord.qlive_utilities.serialisation import build_package, read_package

if __name__ == "__main__":
    print(read_package(build_package(method=QliveRPCMethodEnum.clear_all)))
