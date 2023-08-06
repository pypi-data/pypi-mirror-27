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


class Revoke(Service):
    """
    Mark the given device, or the Project, as Revoked.
    oneID will no longer co-sign for it

    :Example:

        $ oneid-cli revoke --project-id abdc --type edge_device
    """
    def set_up_argparser(self, parser, required):
        if required:
            add_project_id_param(parser)
        else:
            add_device_type_params(parser, False)
            parser.add_argument('--device-id', '-i', type=util.uuid_param, required=False, help='The device UUID')

    def _revoke_device(self, entity_type, entity_id):

        revoke_endpoint = session.REVOKE_PROJECT_ENDPOINT
        if entity_type != 'Project':
            revoke_endpoint = session.REVOKE_SERVER_ENDPOINT
            if entity_type == 'edge_device':
                revoke_endpoint = session.REVOKE_EDGE_DEVICE_ENDPOINT

        revoke_endpoint = revoke_endpoint.format(project_id=self._session.project,
                                                 edge_device_id=entity_id,
                                                 server_id=entity_id)

        try:
            response = self._session.make_api_call(revoke_endpoint, 'POST')
            logger.debug(response)

            if not response or not response['success']:
                print('Error revoking {} {}'.format(entity_type, entity_id))
            else:
                print('Successfully REVOKED {entity_type}: {entity_id}'.format(entity_type=entity_type, entity_id=entity_id))

        except session.HTTPException:
            logger.warning('Error Communicating with oneID - %s', revoke_endpoint, exc_info=True)
            print('Unable to process request -- Error Communicating with oneID')

    def run(self, args):
        """
        Revoke a device or Project

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

            By REVOKING a {thing}, you are telling oneID to never co-sign
            for this {thing} again. This may prevent it from operating,
            accepting updates, etc.

            If a device has been lost, stolen or compromised, this is
            probably what you want, but proceed with awareness.

        """.format(thing='device' if args.type else 'Project')

        entity_id = args.device_id or args.project_id
        entity_type = args.type or 'Project'

        if util.prompt_to_action('REVOKE {} {}'.format(entity_type, entity_id), preamble):
            self._session.project = args.project_id
            self._revoke_device(entity_type, entity_id)

        else:
            print('Revocation cancelled. No changes have been made.')
