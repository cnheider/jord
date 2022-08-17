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

from qgis.core import QgsProject

from jord import PROJECT_NAME

qgis_project = QgsProject.instance()


def restore_default_project_settings(defaults={}, *, project_name=PROJECT_NAME):
    for key, value in defaults.items():
        store_project_setting(key, value, project_name=PROJECT_NAME)


def store_project_setting(key, value, *, project_name=PROJECT_NAME):

    if isinstance(value, bool):
        qgis_project.writeEntryBool(project_name, key, value)
    elif isinstance(value, float):
        qgis_project.writeEntryDouble(project_name, key, value)
    # elif isinstance(value, int): # DOES NOT EXIST!
    #    qgis_project.writeEntryNum(PROJECT_NAME, key, value)
    else:
        value = str(value)
        qgis_project.writeEntry(project_name, key, value)

    print(project_name, key, value)


def read_project_setting(
    key, type_hint=None, *, defaults={}, project_name=PROJECT_NAME
):
    # read values (returns a tuple with the value, and a status boolean
    # which communicates whether the value retrieved could be converted to
    # its type, in these cases a string, an integer, a double and a boolean
    # respectively)

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
