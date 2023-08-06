# Copyright 2017 NEWCRAFT GROUP B.V.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

from confload.ini import IniConfig
from confload.json import JsonConfig
from confload.yaml import YamlConfig


class Config:
    _instance = None

    def __init__(self, file):
        Config.load(file)

    @staticmethod
    def load(file):
        """
        Load a configuration file into memory

        Parameters
        ----------
        file : str
        """
        if ".ini" in file:
            Config._instance = IniConfig
        if ".json" in file:
            Config._instance = JsonConfig
        if ".yaml" in file or ".yml" in file:
            Config._instance = YamlConfig

        Config._instance.load(file)

    @staticmethod
    def ready():
        """
        Checks if a configuration has already been loaded into memory.

        Returns
        -------
        bool
        """
        return Config._instance is not None and Config._instance.ready()

    @staticmethod
    def get(section):

        """
        Parameters
        ----------
        section : str
            The key to retrieve from the configuration file

        Returns
        -------
        dict, str
        """
        return Config._instance.get(section)
