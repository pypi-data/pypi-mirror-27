# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function

import logging

from .. import config_file
from .base import Service, add_project_id_param

logger = logging.getLogger(__name__)


class Show(Service):
    """
    Show project specific information through the command line
    """
    def set_up_argparser(self, parser, required):
        if required:
            add_project_id_param(parser, True)
        else:
            parser.add_argument('--key', '-k', action='store_true', required=False)

    def run(self, args):
        """
        Show the information given the parameters passed in

        :param args: Command Line arguments
        :return: None
        """
        with config_file.load(args.project_id) as config:
            if config and 'AES' in config:
                key = config['AES']
                if args.key and key:
                    print(key)
