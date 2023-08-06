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

from .base import Service, add_project_id_param, add_device_type_params, add_key_manager_params, add_yes_param
from .. import util, session, key_managers
from ..constants import TDIKeyStructureFlags

logger = logging.getLogger(__name__)


class Provision(Service):
    """
    Provision a new device with keys

    :Example:

        $ oneid-cli provision --type edge_device --name my-iot-device --public-key abcdefg

    """
    def set_up_argparser(self, parser, required):
        add_key_manager_params(parser, required)

        if required:
            parser.add_argument('--name', '-n', required=True, help='The name of the device')
            add_project_id_param(parser)
            add_device_type_params(parser)
        else:
            parser.add_argument('--public-key', help='DER formatted public key')
            parser.add_argument('--fleet-keystore', help='Load Fleet keys from existing keystore, if needed')
            add_yes_param(parser)

    def _add_entity_to_project(self, entity_type, entity_name, device_keypair):
        """
        Provision a device to the specified project

        :param entity_type: Either a server or device.
        :param entity_name: Server or Device name.
        :param device_keypair: Keypair for oneID to later validate the entity signature.
        :raises HTTPError: Raised if there are any connection errors
        """
        provisioning_endpoint = session.SERVERS_ENDPOINT.format(project_id=self._session.project)
        if entity_type == 'edge_device':
            provisioning_endpoint = session.EDGE_DEVICES_ENDPOINT.format(project_id=self._session.project)

        public_key_b64 = base64.b64encode(device_keypair.public_key_der).decode('utf-8')

        keys = {entity_type: public_key_b64}
        entity_description = util.aes_encrypt(entity_name, self._session.encryption_key)

        try:
            response = self._session.make_api_call(provisioning_endpoint,
                                                   'POST',
                                                   description=json.dumps(entity_description),
                                                   public_keys=json.dumps(keys),
                                                   project=self._session.project)
            logger.debug(response)

            if not response:
                print('Error provisioning {}'.format(entity_type))
                return

            formatted_type = ' '.join(word.capitalize() for word in entity_type.split('_'))

            resource_name = formatted_type.replace(' ', '') + 's'
            ret = response[resource_name] if resource_name in response else response

            print('Successfully Added {entity_type}: {entity_id}: {entity_name}'.format(
                entity_id=ret['id'],
                entity_type=formatted_type,
                entity_name=entity_name,
            ))
            return ret

        except session.HTTPException:
            logger.warning('Error Communicating with oneID - %s' % provisioning_endpoint, exc_info=True)
            print('Unable to process request -- Error Communicating with oneID')

    def _fleet_keys(self, key_manager, args):
        ret = []

        if args.fleet_keystore:
            logger.debug('loading fleet keys from "%s"', args.fleet_keystore)

            try:
                fleet_keydata = key_manager.load(args.fleet_keystore, args.project_id)

                for rec in fleet_keydata:
                    rec['skip_private'] = True

                ret += fleet_keydata

            except NotImplementedError:
                logger.warning("Fleet keystore not supported for this keystore type")

            except (IOError, OSError):
                print("Fleet keystore {} not available, ignoring".format(args.fleet_keystore))

        return ret

    def run(self, args):
        """
        Provision a device with a set of identity keys.
        If output not specified, print to console
        If public key not specified, generate a private key and save to output

        :param args: command line argument parser args
        """
        self._session.project = args.project_id

        device_keypair = None
        if args.public_key:
            # TODO: Specify public key type
            device_keypair = oneid.keychain.Keypair.from_public_der(base64.b64decode(args.public_key))
        elif args.yes:
            logger.debug('automatically creating keys.')
            device_keypair = oneid.service.create_secret_key()
        else:
            print('No public key specified.')
            device_keypair = util.prompt_to_create_keypair()

        if not device_keypair:
            print('No public key given or generated. Unable to create "{}"'.format(args.name))
            return

        entity = self._add_entity_to_project(args.type, args.name, device_keypair)

        if entity:
            entity_keypair = device_keypair if not args.public_key else False

            if entity_keypair:
                kmgrargs = args.keymgr if args.keymgr else []
                key_manager = key_managers.get_key_manager(*kmgrargs)
                role = (TDIKeyStructureFlags.ROLE_SERVER if args.type == 'server' else TDIKeyStructureFlags.ROLE_DEVICE)
                keypair_list = [{
                    'name': args.name,
                    'skip_private': True if args.public_key else False,
                    'keypair': entity_keypair,
                    'tdi_type': args.type,
                    'tdi_id': entity['id'],
                    'flags': (role | TDIKeyStructureFlags.CAN_SIGN | TDIKeyStructureFlags.OUR_OWN),
                }] + self._fleet_keys(key_manager, args)

                if args.keystore:
                    try:
                        key_manager.save(args.keystore, entity['project'], keypair_list)
                    except EnvironmentError as e:
                        print('Error saving keys: {}'.format(e))
                else:
                    key_manager.show(entity['project'], keypair_list, args.yes)
