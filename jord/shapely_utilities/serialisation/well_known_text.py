from pathlib import Path
from typing import Sequence
import pandas
from shapely import wkt
from pandas import DataFrame

__all__ = ["load_wkts_from_csv", "csv_wkt_generator"]


def load_wkts_from_csv(
    csv_file_path: Path, geometry_column: str = "Shape", additional_cols: Sequence = ()
) -> DataFrame:
    """
    Well-Known Text
    """
    df = pandas.read_csv(
        str(csv_file_path), usecols=[*additional_cols, geometry_column]
    )
    df[geometry_column] = df[geometry_column].apply(wkt.loads)
    return df


def csv_wkt_generator(csv_file_path: Path, geometry_column: str = "Shape") -> wkt:
    for idx, g in pandas.read_csv(
        str(csv_file_path), usecols=[geometry_column]
    ).iterrows():
        yield wkt.loads(g)
