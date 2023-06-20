# !/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 5/5/22
           """

__all__ = [
    "store_project_setting",
    "read_project_setting",
    "restore_default_project_settings",
]

from logging import warning
from typing import Any, Mapping, Optional

from qgis.core import QgsProject

from jord import PROJECT_NAME

qgis_project = QgsProject.instance()


def restore_default_project_settings(
    defaults: Optional[Mapping] = None, *, project_name: str = PROJECT_NAME
):
    """

    :param defaults:
    :param project_name:
    :return:
    """
    if defaults is None:
        defaults = {}
    for key, value in defaults.items():
        store_project_setting(key, value, project_name=project_name)


def store_project_setting(key: str, value: Any, *, project_name: str = PROJECT_NAME):
    """

    :param key:
    :param value:
    :param project_name:
    :return:
    """
    if isinstance(value, bool):
        qgis_project.writeEntryBool(project_name, key, value)
    elif isinstance(value, float):
        qgis_project.writeEntryDouble(project_name, key, value)
    # elif isinstance(value, int): # DOES NOT EXIST!
    #    qgis_project.writeEntryNum(project_name, key, value)
    else:
        value = str(value)
        qgis_project.writeEntry(project_name, key, value)

    print(project_name, key, value)


def read_project_setting(
    key: str,
    type_hint: type = None,
    *,
    defaults: Mapping = None,
    project_name: str = PROJECT_NAME,
):
    """

    :param key:
    :param type_hint:
    :param defaults:
    :param project_name:
    :return:
    """

    # read values (returns a tuple with the value, and a status boolean
    # which communicates whether the value retrieved could be converted to
    # its type, in these cases a string, an integer, a double and a boolean
    # respectively)

    if defaults is None:
        defaults = {}

    if type_hint is not None:
        if type_hint is bool:
            val, type_conversion_ok = qgis_project.readBoolEntry(
                project_name, key, defaults.get(key, None)
            )
        elif type_hint is float:
            val, type_conversion_ok = qgis_project.readDoubleEntry(
                project_name, key, defaults.get(key, None)
            )
        elif type_hint is int:
            val, type_conversion_ok = qgis_project.readNumEntry(
                project_name, key, defaults.get(key, None)
            )
        else:
            val, type_conversion_ok = qgis_project.readEntry(
                project_name, key, str(defaults.get(key, None))
            )
    else:
        val, type_conversion_ok = qgis_project.readEntry(
            project_name, key, str(defaults.get(key, None))
        )

    if type_hint is not None:
        val = type_hint(val)

    if False:
        if not type_conversion_ok:
            warning(f"read_plugin_setting: {key} {val} {type_conversion_ok}")

    return val
