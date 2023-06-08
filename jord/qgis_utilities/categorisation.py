import json
import random
from itertools import cycle
from typing import Any, Generator
from typing import Iterable

from PyQt5.Qt import QColor
from qgis.core import (
    QgsVectorLayer,
    QgsSymbol,
    QgsRendererCategory,
    QgsCategorizedSymbolRenderer,
)
from warg import TripleNumber

__all__ = ["categorise_layer", "categorise_layer_from_json"]


def categorise_layer_from_json(
    layer: QgsVectorLayer,
    color_mapping_json: str,
    field_name: str = "layer",
    default_color: TripleNumber = (0, 0, 0),
) -> None:
    color_mapping = json.loads(color_mapping_json)[field_name]

    render_categories = []
    for cat in layer.uniqueValues(layer.fields().indexFromName(field_name)):
        cat_color = default_color
        if cat in color_mapping.keys():
            cat_color = (int(n) for n in color_mapping[cat])

        sym = QgsSymbol.defaultSymbol(layer.geometryType())
        sym.setColor(QColor(*(cat_color), 255))
        render_categories.append(
            QgsRendererCategory(cat, symbol=sym, label=cat, render=True)
        )

    layer.setRenderer(QgsCategorizedSymbolRenderer(field_name, render_categories))
    layer.triggerRepaint()


def random_rgb(mix: TripleNumber = (255, 255, 255)) -> TripleNumber:
    red = random.randrange(0, mix[0])
    green = random.randrange(0, mix[1])
    blue = random.randrange(0, mix[2])
    return (red, green, blue)


def random_rgba(mix: TripleNumber = (1, 1, 1, 1)) -> TripleNumber:
    red = random.randrange(0, mix[0])
    green = random.randrange(0, mix[1])
    blue = random.randrange(0, mix[2])
    alpha = random.randrange(0, mix[3])
    return (red, green, blue, alpha)


def random_color_generator() -> Any:
    while 1:
        yield random_rgb()


from typing import Sized


def categorise_layer(
    layer: QgsVectorLayer,
    field_name: str = "layer",
    iterable: Iterable = random_color_generator,
) -> None:
    if isinstance(iterable, Sized):
        iterable = cycle(iterable)
    color_iter = iter(iterable())

    render_categories = []
    for cat in layer.uniqueValues(layer.fields().indexFromName(field_name)):
        sym = QgsSymbol.defaultSymbol(layer.geometryType())
        sym.setColor(QColor(*(next(color_iter)), 255))
        render_categories.append(
            QgsRendererCategory(cat, symbol=sym, label=cat, render=True)
        )

    layer.setRenderer(QgsCategorizedSymbolRenderer(field_name, render_categories))
    layer.triggerRepaint()
