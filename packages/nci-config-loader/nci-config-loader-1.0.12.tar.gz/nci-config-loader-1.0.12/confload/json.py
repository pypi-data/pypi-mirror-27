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

import json


class JsonConfig:
    """
    Json config file loader
    """
    data = {}

    @staticmethod
    def load(file):
        """
        Parameters
        ----------
        file : str
            The file to load
        """
        with open(file, 'r') as jsonfile:
            JsonConfig.data = json.load(jsonfile)

    @staticmethod
    def ready():
        """
        Returns
        -------
        bool
        """
        return len(JsonConfig.data) > 0

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
        return JsonConfig.data[section]
