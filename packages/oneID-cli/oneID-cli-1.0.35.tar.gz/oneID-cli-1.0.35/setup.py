# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os

from setuptools import setup, find_packages
from codecs import open


base_dir = os.path.dirname(__file__)

with open(os.path.join(base_dir, "README.rst")) as f:
    long_description = f.read()

setup(
    name='oneID-cli',
    version='1.0.35',
    description='A command line interface for the Neustar Trusted Identity (TDI) Core',
    long_description=long_description,
    url='https://www.oneID.com',
    author='Neustar Inc.',
    author_email='support@oneID.com',
    license='Apache License, Version 2.0',
    classifiers=[
        'Development Status :: 4 - Beta',
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX",
        "Operating System :: POSIX :: BSD",
        "Operating System :: POSIX :: Linux",
        'Topic :: Security :: Cryptography',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],

    keywords='TDI IoT Identity Authentication',
    package_dir={"": "src"},
    packages=find_packages(where='src',
                           exclude=['contrib', 'docs', 'tests*',
                                    'venv', 'example*']),
    install_requires=[
        'oneID-connect>=0.21.1,<0.22', 'pyOpenSSL>=17.3.0,<18',
        'requests[security]>=2.18.4,<2.19',
        'ruamel.yaml>=0.15.34,<0.16',
        'six>=1.11.0,<1.12',
        'setuptools>=38.2.4',
    ],
    scripts=['bin/oneid-cli'],

)
