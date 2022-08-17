__all__ = ["disconnect_signal", "connect_signal", "reconnect_signal"]

from logging import warning

from qgis.PyQt import QtCore

IS_DEBUGGING = False


def connect_signal(signal: QtCore.pyqtSignal, new_handler: callable = None) -> None:
    if new_handler is not None:  # if newhandler is not None, connect it
        signal.connect(new_handler)
    else:
        if IS_DEBUGGING:
            raise Exception("new_handler is None")
        warning("new_handler is None")


def disconnect_signal(signal: QtCore.pyqtSignal, old_handler: callable = None) -> None:
    if signal is not None:
        try:
            if old_handler is not None:  # disconnect oldhandler(s)
                while True:
                    # the loop is needed for safely disconnecting a specific handler,
                    # because it may have been connected multple times,
                    # and disconnect(slot) only removes one connection at a time.
                    signal.disconnect(old_handler)
            else:  # disconnect all, only available when old_handler is None and we are debugging, as this is bad practice
                if IS_DEBUGGING:
                    signal.disconnect()
        except TypeError:
            pass


def reconnect_signal(
    signal: QtCore.pyqtSignal,
    new_handler: callable = None,
    old_handler: callable = None,
) -> None:
    disconnect_signal(signal, old_handler)
    connect_signal(signal, new_handler)
