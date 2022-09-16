#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02-12-2020
           """

from pathlib import Path

__all__ = ["install_requirements_from_file", "install_requirements_from_name"]

from typing import Iterable


def install_requirements_from_file(requirements_path: Path) -> None:
    """
    Install requirements from a requirements.txt file.

    :param requirements_path: Path to requirements.txt file.

    """

    # pip.main(["install", "pip", "--upgrade"]) # REQUIRES RESTART OF QGIS

    args = ["install", "-r", str(requirements_path), "--upgrade"]
    # args = ["install", "rasterio", "--upgrade"] # RASTERIO for window DOES NOT WORK ATM, should be installed manually

    if False:
        import pip

        pip.main(args)

    elif False:
        from subprocess import call

        call(["pip"] + args)

    elif True:
        from subprocess import call

        call(["python", "-m", "pip"] + args)


def install_requirements_from_name(requirements_name: Iterable[str]) -> None:
    """
    Install requirements from names.

    :param requirements_name: Name of requirements.
    """
    # pip.main(["install", "pip", "--upgrade"]) # REQUIRES RESTART OF QGIS

    args = ["install", *requirements_name, "--upgrade"]
    # args = ["install", "rasterio", "--upgrade"] # RASTERIO for window DOES NOT WORK ATM, should be installed manually

    if False:
        import pip

        pip.main(args)

    elif False:
        from subprocess import call

        call(["pip"] + args)

    elif True:
        from subprocess import call

        call(["python", "-m", "pip"] + args)
