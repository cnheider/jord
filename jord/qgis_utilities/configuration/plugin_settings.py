#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02-12-2020
           """

__all__ = ["store_plugin_setting", "read_plugin_setting"]

from qgis.core import QgsSettings

from jord import PROJECT_NAME


def store_plugin_setting(key, value, *, project_name=PROJECT_NAME):
    QgsSettings().setValue(f"{project_name}/{key}", value)


def read_plugin_setting(key, *, default_value=None, project_name=PROJECT_NAME):
    return QgsSettings().value(f"{project_name}/{key}", default_value)


if __name__ == "__main__":
    store_plugin_setting("mytext", "hello world")
    print(read_plugin_setting("mytext"))
