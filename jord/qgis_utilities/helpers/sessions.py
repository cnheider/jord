from qgis.core import QgsMapLayer
from warg import AlsoDecorator

__all__ = ["QLayerEditSession"]


class QLayerEditSession(AlsoDecorator):
    def __init__(self, qlayer: QgsMapLayer):
        self.qlayer = qlayer

    def __enter__(self):
        if self.qlayer:
            self.qlayer.startEditing()
        return True

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.qlayer:
            self.qlayer.commitChanges()
