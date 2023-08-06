# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import json
import base64
import logging

import six

import oneid

from .. import config_file, session
from .base import Service, add_project_id_param, add_yes_param

logger = logging.getLogger(__name__)


class Configure(Service):
    """
    Store json dump of credentials in ~/.oneid/credentials

    :Example:

        $ oneid-cli configure

    """
    def set_up_argparser(self, parser, required):
        if not required:
            exclusion_group = parser.add_mutually_exclusive_group()
            add_project_id_param(exclusion_group, False)
            exclusion_group.add_argument('--name', '-n', help='A name or description for the Project Admin')
            add_yes_param(parser)

    def update_project_credentials(self, project_id, aes_key):
        """
        Create or update stored Project configuration data

        :param project_id: Project to update
        :param aes_key: Project's encryption key, base64-encoded (non-URL-safe) DER-formatted AES256 key
        :type project_id: str()
        :type aes_key: str()
        """
        with config_file.update(project_id) as credentials:
            credentials['AES'] = aes_key

    def create_credentials(self, description=None):
        """
        Create a new ProjectAdmin and update configuration

        :param description: Name or description to label the Project Admin with (optional)
        :type description: str()
        """
        try:
            with config_file.load() as config:
                if 'PROJECT_ADMIN' in config:
                    raise RuntimeError('Project Admin already configured')
        except ValueError:
            pass

        keypair = oneid.service.create_secret_key()
        public_key_der_b64 = base64.b64encode(keypair.public_key_der).decode('utf-8')
        private_key_der_b64 = base64.b64encode(keypair.secret_as_der).decode('utf-8')

        keys = {'project_admin': public_key_der_b64}

        try:
            self_signed_session = session.SelfSignedSession(keypair, 'project_admin')
            response = self_signed_session.make_api_call(
                session.PROJECT_ADMINS_ENDPOINT,
                'POST',
                description=description,
                public_keys=json.dumps(keys),
            )

            if not response:
                print('Error creating ProjectAdmin')
                return
            logger.debug(response)

            ret = response.get('ProjectAdmins', response)

            print('Successfully Created Project Admin: {id}: {description}'.format(id=ret['id'], description=ret.get('description')))

            self.update_project_admin_credentials(ret['id'], private_key_der_b64, ret['public_keys']['project_admin_return'])

        except session.HTTPException:
            logger.warning('Error Communicating with NTDI Core Server: %s' % session.PROJECT_ADMINS_ENDPOINT, exc_info=True)
            print('Unable to process request -- Error Communicating with NTDI Core Server')

    def update_project_admin_credentials(self, project_admin_id, access_secret, return_key, alt_session=None):
        """
        Create or update stored ProjectAdmin configuration data

        :param project_admin_id: oneID Developer portal ID for the project admin
        :param access_secret: ProjectAdmin's secret key, DER-formatted private key
        :type project_admin_id: str()
        :type access_secret: str()
        """
        if project_admin_id is None or access_secret is None:
            raise ValueError('Access ID and Access Secret are required to configure')

        with config_file.update() as config:
            credentials = config.get('PROJECT_ADMIN', {})
            credentials['ID'] = project_admin_id
            credentials['SECRET'] = access_secret
            credentials['RETURN_KEY'] = return_key

            base_url = (alt_session or self._session).base_url

            if base_url != session.DEFAULT_BASE_URL:
                config['URL'] = base_url

            config['PROJECT_ADMIN'] = credentials

    def run(self, args):
        project_id = args.project_id
        if project_id:
            if args.yes:
                project_encryption_key = base64.b64encode(oneid.service.create_aes_key()).decode('utf-8')
            else:
                project_encryption_key = six.moves.input('PROJECT ENCRYPTION KEY: ')
            self.update_project_credentials(project_id, project_encryption_key)
        elif args.yes:
            self.create_credentials(args.name)
        else:
            project_admin_id = six.moves.input('ONEID ACCESS ID: ')
            access_secret = six.moves.input('ONEID ACCESS SECRET: ')
            return_key = six.moves.input('ONEID ACCESS RETURN KEY: ')
            self.update_project_admin_credentials(project_admin_id, access_secret, return_key)
