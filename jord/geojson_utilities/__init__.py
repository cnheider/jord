from pathlib import Path

try:
    from .geometry_types import *


except ImportError as ix:
    this_package_name = Path(__file__).parent.name
    print(f"Make sure geopandas module is available for {this_package_name}")
    raise ix
