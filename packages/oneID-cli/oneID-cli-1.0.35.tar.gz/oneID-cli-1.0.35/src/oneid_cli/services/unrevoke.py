# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function

import logging

from .. import util, session
from .base import Service, add_project_id_param, add_device_type_params

logger = logging.getLogger(__name__)


class Unrevoke(Service):
    """
    Mark the given device, or the Project, as Active.
    oneID will co-sign for it, if it wasn't already

    :Example:

        $ oneid-cli unrevoke --project-id abdc --type edge_device
    """
    def set_up_argparser(self, parser, required):
        if required:
            add_project_id_param(parser)
        else:
            add_device_type_params(parser, False)
            parser.add_argument('--device-id', '-i', type=util.uuid_param, required=False, help='The device UUID')

    def _unrevoke_device(self, entity_type, entity_id):

        unrevoke_endpoint = session.UNREVOKE_PROJECT_ENDPOINT
        if entity_type != 'Project':
            unrevoke_endpoint = session.UNREVOKE_SERVER_ENDPOINT
            if entity_type == 'edge_device':
                unrevoke_endpoint = session.UNREVOKE_EDGE_DEVICE_ENDPOINT

        unrevoke_endpoint = unrevoke_endpoint.format(project_id=self._session.project,
                                                     edge_device_id=entity_id,
                                                     server_id=entity_id)

        try:
            response = self._session.make_api_call(unrevoke_endpoint, 'POST')
            logger.debug(response)

            if not response or not response['success']:
                print('Error unrevoking {} {}'.format(entity_type, entity_id))
            else:
                print('Successfully UNREVOKED {entity_type}: {entity_id}'.format(entity_type=entity_type, entity_id=entity_id))

        except session.HTTPException:
            logger.warning('Error Communicating with oneID - %s', unrevoke_endpoint, exc_info=True)
            print('Unable to process request -- Error Communicating with oneID')

    def run(self, args):
        """
        Unrevoke a device or Project

        :param args: command line argument parser args
        """

        if args.type and not args.device_id:
            args.parser.error('--device-id required if --type specified')
            return

        if args.device_id and not args.type:
            args.parser.error('--type required if --device-id specified')
            return

        preamble = """
            *** WARNING ***

            By UNREVOKING a {thing}, you are now telling oneID to co-sign
            for this {thing} again.

            If a device has been restored from a lost or compromised state, this is
            probably what you want, but proceed with awareness.

        """.format(thing='device' if args.type else 'Project')

        entity_id = args.device_id or args.project_id
        entity_type = args.type or 'Project'

        if util.prompt_to_action('UNREVOKE {} {}'.format(entity_type, entity_id), preamble):
            self._session.project = args.project_id
            self._unrevoke_device(entity_type, entity_id)

        else:
            print('Unrevocation cancelled. No changes have been made.')
