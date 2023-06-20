from qgis.core import QgsMapLayer
from warg import AlsoDecorator

__all__ = ["QLayerEditSession"]


class QLayerEditSession(AlsoDecorator):
    def __init__(self, map_layer: QgsMapLayer):
        self.map_layer = map_layer

    def __enter__(self):
        if self.map_layer:
            self.map_layer.startEditing()
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.map_layer:
            self.map_layer.commitChanges()
