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
import configparser

from pkg_resources import packaging
from pathlib import Path

from qgis.gui import QgisInterface
from qgis.core import QgsSettings
from qgis.PyQt.QtWidgets import QMessageBox

# NEW_FOLDER is the zip name from a loaded repository in QGIS

# url to add, where to load new plugin from
URL = "https://your/url/plugins.xml"

# old plugins folder, e.g. "Path(__file__).parent" <- this folder
OLD_FOLDER = ""

# new plugin key/zip file name from a loaded repository
NEW_FOLDER = ""


class PluginRepoUrlChanged:

    def __init__(self, iface: QgisInterface, *args, **kwargs: dict):

        self.iface: QgisInterface = iface
        self.metadata_path = Path(__file__).parent / "metadata.txt"
        self.version = self.get_local_version()
        self.name = self.get_meta_value('name')

    # noinspection PyPep8Naming
    def initGui(self):
        import qgis.utils
        from pyplugin_installer import instance
        pluginInstaller = instance()

        self.add_new_repository()
        pluginInstaller.fetchAvailablePlugins(True)

        if not Path(OLD_FOLDER).exists():
            return

        # uninstall me?!
        pluginInstaller.uninstallPlugin(OLD_FOLDER, quiet=True)

        if NEW_FOLDER not in qgis.utils.plugins:
            pluginInstaller.installPlugin(NEW_FOLDER, quiet=True)

    def unload(self, self_unload: bool = False):
        """ nothing special to unload here """


    def get_local_version(self) -> str:
        """ Reads local version string from local metadata.txt """
        version_str = self.get_meta_value('version')
        version_obj = packaging.version.parse(version_str)
        return version_obj

    def get_meta_value(self, key: str) -> str:
        """ Reads a value from metadata.txt.

            :param key: key in 'general' section
        """

        config = configparser.ConfigParser()
        config.read(self.metadata_path, encoding='utf-8')
        return config['general'][key]

    def add_new_repository(self):
        from pyplugin_installer.installer_data import reposGroup

        if not URL:
            return

        settings = QgsSettings()
        settings.beginGroup(reposGroup)

        for key in settings.childGroups():
            current_url = settings.value(key + "/url", "", type=str)
            if current_url == URL:
                print("alread added")
                return

        # lets add the new group
        key = "New Plugin URL"
        settings.setValue(key + "/url", URL)
        settings.setValue(key + "/authcfg", "")
        settings.setValue(key + "/enabled", "true")
        settings.endGroup()
        settings.sync()
