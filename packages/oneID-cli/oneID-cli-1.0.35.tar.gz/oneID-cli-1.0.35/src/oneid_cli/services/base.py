# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import logging

from .. import util
from ..key_managers import KeyManagerType, KeyManagerSubType

logger = logging.getLogger(__name__)


class Service(object):
    """
    Base Service that all services subclass

    :param session: session that manages the current user's
      credentials and settings
    :type session: session.CLISession
    """
    request_uri = None

    def __init__(self, active_session):
        self._session = active_session

    def set_up_argparser(self, parser, required):
        """
        oneid-cli will create the main argument parser and subparsers
        each Service will be able to specify additional, Service-specific arguments, if needed
        """
        pass

    def run(self, args):
        """
        oneid-cli will first parse for the service
        if a valid service is found, it will pass the remaining
        args to the service for the service to parse
        """
        logger.warning('Attempt to call unimplemented Service')
        raise NotImplementedError


# Some common parameters that can be shared across Services
#
def add_project_id_param(parser, required=True):
    parser.add_argument('--project-id', '-p', type=util.uuid_param, required=required, help='Specify a project using oneID project UUID')


def add_device_type_params(parser, required=True):
    parser.add_argument('--type', '-t', choices=['edge_device', 'server'], required=required, help='Type of device')


# slighty different semantics here for 'required'
def add_key_manager_params(parser, required):
    if not required:
        parser.add_argument('--keystore', '--output-dir', '-o', help='Keystore to write keys to (Note: --output-dir is deprecated)')

        keystore_group = parser.add_mutually_exclusive_group(required=False)
        keystore_group.add_argument('--use-pem-keystore', '-P',
                                    action='store_const', dest='keymgr', const=[KeyManagerType.NTDI, KeyManagerSubType.PEM],
                                    help='If given, save/load keys from TDI keystore (PEM format)',
                                    )
        keystore_group.add_argument('--use-jwk-keystore', '-J',
                                    action='store_const', dest='keymgr', const=[KeyManagerType.NTDI, KeyManagerSubType.JWK],
                                    help='If given, save/load keys from TDI keystore (JWK format)',
                                    )


def add_yes_param(parser):
    parser.add_argument('-y', '--yes',
                        action='store_true',
                        help='Automatically create new keys/credentials without prompting.')
