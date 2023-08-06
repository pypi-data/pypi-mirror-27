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

import configparser


class IniConfig:
    parser = configparser.ConfigParser()

    @staticmethod
    def load(file):
        """
        Parameters
        ----------
        file : str
            The file to load
        """
        IniConfig.parser = configparser.ConfigParser()
        IniConfig.parser.read(file)

    @staticmethod
    def ready():
        """
        Returns
        -------
        bool
        """
        return len(IniConfig.parser.sections()) > 0

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
        dict1 = {}
        options = IniConfig.parser.options(section)
        for option in options:
            try:
                dict1[option] = IniConfig.parser.get(section, option)
                if dict1[option] == -1:
                    print("skip: %s" % option)
            except:
                print("exception on %s!" % option)
                dict1[option] = None
        return dict1
