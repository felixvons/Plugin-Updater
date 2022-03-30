# -*- coding: utf-8 -*-

"""
***************************************************************************
    plugin.py            ---------------------
    Date                 : March 2022
    Copyright            : (C) 2022 Felix von Studsinske
    Email                : felix dot vons at gmail dot com
                           (felix.vons@gmail.de)
    Developer            : Felix von Studsinske
    Description          :
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
"""
from qgis.gui import QgisInterface
from typing import Type

# Edit this import and references in this file to new name
from .plugin import PluginRepoUrlChanged


def get_class() -> Type[PluginRepoUrlChanged]:
    """ returns plugin class """
    return PluginRepoUrlChanged


# noinspection PyPep8Naming
def classFactory(iface: QgisInterface, **kwargs: dict) -> PluginRepoUrlChanged:  # pylint: disable=invalid-name
    """Loads this plugin an loads it. Automatically called by QGIS

    :param iface: A QGIS interface instance.
    """

    return get_class()(iface, **kwargs)
