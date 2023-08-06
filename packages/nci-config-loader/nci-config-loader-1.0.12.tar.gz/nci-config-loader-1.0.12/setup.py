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

from setuptools import setup, find_packages

setup(
    name='nci-config-loader',
    version='1.0.12',
    description='Configuration file loader and parser',
    author='Newcraft',
    author_email='cedric.le.varlet@newcraftgroup.com',
    url='https://github.com/newcraftgroup/nci-python-config',
    download_url='https://github.com/newcraftgroup/nci-python-config/tarball/master',
    license='Apache License, Version 2.0',
    packages=find_packages(),
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 3'
                 ],
    install_requires=["PyYAML"]
)
