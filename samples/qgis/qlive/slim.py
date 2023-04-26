import zmq

from jord.qlive_utilities.serialisation import build_package
from jord.qlive_utilities.procedures import QliveRPCMethodEnum

context = zmq.Context()

socket = context.socket(zmq.REQ)

socket.connect("tcp://localhost:5555")

DEFAULT_CRS = "EPSG:3857"  # "EPSG:4326"
crs = DEFAULT_CRS

example_wkt_polygon = (
    "POLYGON((10.689697265625 -25.0927734375, 34.595947265625 "
    "-20.1708984375, 38.814697265625 -35.6396484375, 13.502197265625 "
    "-39.1552734375, 10.689697265625 -25.0927734375))"
)
example_wkt_polygon2 = "POLYGON ((30 10, 10 20, 20 40, 40 40, 30 10))"

example_wkt_gm = (
    "GEOMETRYCOLLECTION(POINT(0 0), LINESTRING(0 0, 1440 900), POLYGON((0 0, 0 1024, 1024 1024, "
    "1024 0, 0 0)))"
)

if True:
    socket.send(build_package(QliveRPCMethodEnum.add_wkt, example_wkt_polygon))
    print("sent")
    message = socket.recv()
    print(message)

if True:
    socket.send(build_package(QliveRPCMethodEnum.add_wkt, example_wkt_gm))
    print("sent")
    message = socket.recv()
    print(message)
