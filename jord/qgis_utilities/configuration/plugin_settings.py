#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02-12-2020
           """

__all__ = ["store_plugin_setting", "read_plugin_setting"]

from typing import Any

from qgis.core import QgsSettings

from jord import PROJECT_NAME


def store_plugin_setting(key: str, value: Any, *, project_name: str = PROJECT_NAME):
    """

    :param key:
    :param value:
    :param project_name:
    :return:
    """
    QgsSettings().setValue(f"{project_name}/{key}", value)


def read_plugin_setting(
    key: str, *, default_value: Any = None, project_name: str = PROJECT_NAME
):
    """

    :param key:
    :param default_value:
    :param project_name:
    :return:
    """
    return QgsSettings().value(f"{project_name}/{key}", default_value)


if __name__ == "__main__":
    store_plugin_setting("mytext", "hello world")
    print(read_plugin_setting("mytext"))
