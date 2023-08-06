# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function

import json
import base64
import logging

import oneid.keychain
import oneid.service

from .base import Service, add_key_manager_params, add_yes_param
from .. import util, session, config_file, key_managers
from ..constants import TDIKeyStructureFlags

logger = logging.getLogger(__name__)


class CreateProject(Service):
    """
    Start a new Project with keys
    Configuration will be updated with new Project data

    :Example:

        $ oneid-cli create-project --name my-iot-project --aes-key ae5f6d

    """
    def set_up_argparser(self, parser, required):
        add_key_manager_params(parser, required)

        if required:
            parser.add_argument('--name', '-n', required=True, help='The name of the Project')
        else:
            parser.add_argument('--aes-key', help='base64-encoded AES encryption key (if not specified, one will be generated)')
            parser.add_argument('--public-key', help='DER formatted public key')
            add_yes_param(parser)

    def _create_project(self, project_name, aes_key, project_keypair):
        """
        Create a new Project

        :param project_name: Server or Device name.
        :returns: created Project fields
        :rtype: dict
        :raises :py:class:session.HTTPException: Raised if there are any connection errors
        """
        project = None

        api_endpoint = session.PROJECTS_ENDPOINT

        public_key_b64 = base64.b64encode(project_keypair.public_key_der).decode('utf-8')

        keys = {'project': public_key_b64}
        description = util.aes_encrypt(project_name, aes_key)

        project_admin_id = self._session.keypair.identity
        project_admins = [project_admin_id]

        try:
            response = self._session.make_api_call(api_endpoint, 'POST',
                                                   description=json.dumps(description),
                                                   project_admins=project_admins,
                                                   public_keys=json.dumps(keys),
                                                   project=self._session.project)
            logger.debug(response)

            project = response and response.get('Projects', response)

            if project:
                description = json.loads(project['description'])

                try:
                    project['description'] = oneid.service.decrypt_attr_value(description, aes_key).decode('utf-8')
                except:  # noqa: E422
                    logger.debug('Exception decrypting freshly-saved Project description', exc_info=True)
                    project['description'] = '(encrypted)'

                project['public_keys'] = json.loads(project['public_keys'])

                print('Successfully Added Project: {id}: {description}'.format(**project))

                with config_file.update(project['id']) as configuration:
                    configuration['AES'] = str(base64.b64encode(aes_key).decode('utf-8'))
            else:
                print('Error creating Project')
                return None

        except session.HTTPException:
            logger.warning('Error Communicating with oneID - %s', api_endpoint, exc_info=True)
            print('Unable to process request -- Error Communicating with oneID')

        return project

    def run(self, args):
        """
        Create a project.

        :param args: command line argument parser args
        """
        aes_key = None
        if args.aes_key:
            aes_key = base64.b64decode(args.aes_key)
        else:
            aes_key = oneid.service.create_aes_key()

        project_keypair = None
        if args.public_key:
            # TODO: Specify public key type
            project_keypair = oneid.keychain.Keypair.from_public_der(base64.b64decode(args.public_key))
        elif args.yes:
            logger.debug('automatically creating keys.')
            project_keypair = oneid.service.create_secret_key()
        else:
            print('No public key specified.')
            project_keypair = util.prompt_to_create_keypair()

        if not project_keypair:
            print('No public key given or generated. Unable to create "{}"'.format(args.name))
            return

        project = self._create_project(args.name, aes_key, project_keypair)

        if project:
            kmgrargs = args.keymgr if args.keymgr else []
            key_manager = key_managers.get_key_manager(*kmgrargs)
            keypair_list = [
                {
                    'name': 'Core Fleet',
                    'skip_private': True,
                    'keypair': oneid.keychain.Keypair.from_public_der(base64.b64decode(project['public_keys']['oneid_project'])),
                    'flags': TDIKeyStructureFlags.ROLE_F_C,
                },
                {
                    'name': 'Fleet',
                    'skip_private': True if args.public_key else False,
                    'keypair': project_keypair,
                    'flags': TDIKeyStructureFlags.ROLE_F_S | TDIKeyStructureFlags.CAN_SIGN,
                },
            ]

            if args.keystore:
                try:
                    key_manager.save(args.keystore, project['id'], keypair_list)
                except EnvironmentError as e:
                    print('Error saving keys: {}'.format(e))
            else:
                key_manager.show(project['id'], keypair_list, args.yes)
