# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
import re
import requests
import base64
import json
import logging

from oneid import keychain, jose, jwts, nonces, utils

from . import config_file

logger = logging.getLogger(__name__)


DEFAULT_BASE_URL = 'https://api.oneid.com'

PROJECT_ADMINS_ENDPOINT = '/project_admins'

PROJECTS_ENDPOINT = '/projects'
PROJECT_ENDPOINT = PROJECTS_ENDPOINT + '/{project_id}'
REVOKE_PROJECT_ENDPOINT = PROJECT_ENDPOINT + '/revoke'
UNREVOKE_PROJECT_ENDPOINT = PROJECT_ENDPOINT + '/unrevoke'

SERVERS_ENDPOINT = PROJECT_ENDPOINT + '/servers'
SERVER_ENDPOINT = SERVERS_ENDPOINT + '/{server_id}'
REVOKE_SERVER_ENDPOINT = SERVER_ENDPOINT + '/revoke'
UNREVOKE_SERVER_ENDPOINT = SERVER_ENDPOINT + '/unrevoke'

EDGE_DEVICES_ENDPOINT = PROJECT_ENDPOINT + '/edge_devices'
EDGE_DEVICE_ENDPOINT = EDGE_DEVICES_ENDPOINT + '/{edge_device_id}'
REVOKE_EDGE_DEVICE_ENDPOINT = EDGE_DEVICE_ENDPOINT + '/revoke'
UNREVOKE_EDGE_DEVICE_ENDPOINT = EDGE_DEVICE_ENDPOINT + '/unrevoke'


class HTTPException(requests.exceptions.RequestException):
    pass


class CLISession(object):
    """
    Manage the active user's configuration and credentials

    :param project_name: Optional project name for settings
        specific to a project
    """
    def __init__(self, project_id=None):
        self._base_url = None
        self._project_id = project_id
        self._encryption_key = None
        self._keypair = None
        self._return_keypair = None

    @property
    def base_url(self):
        if not self._base_url:
            self._base_url = os.environ.get('NTDI_CORE_SERVER_BASE_URL', os.environ.get('ONEID_API_SERVER_BASE_URL'))

        if not self._base_url:
            try:
                with config_file.load() as config:
                    self._base_url = config and config.get('URL') or DEFAULT_BASE_URL
                    logger.debug('base url=%s', self._base_url)
            except:  # noqa: E422
                self._base_url = DEFAULT_BASE_URL

        return self._base_url

    @property
    def project(self):
        return self._project_id

    @project.setter
    def project(self, value):
        self._project_id = value

    @property
    def keypair(self):
        return self._keypair or self.get_keypair()

    @property
    def return_keypair(self):
        if self._return_keypair is None:
            self._load_project_admin_settings()

        return self._return_keypair

    @property
    def encryption_key(self):
        if self._encryption_key is None and self._project_id:
            self._load_project_settings()

        return self._encryption_key

    def _load_project_settings(self):
        """
        Given a project id, load settings
        :return:
        """
        with config_file.load(self.project) as project_credentials:
            if project_credentials is None:
                raise ValueError('Could not find any valid credentials for %s project' % self.project)

            self._encryption_key = 'AES' in project_credentials and utils.base64url_decode(project_credentials['AES'])

    def _load_project_admin_settings(self):
        """
        Load ProjectAdmin settings
        :return:
        """
        with config_file.load() as credentials:
            project_admin_credentials = credentials and credentials.get('PROJECT_ADMIN')
            logger.debug('project_admin_credentials=%s', project_admin_credentials)
            if not project_admin_credentials:
                raise ValueError('Could not find any valid credentials, please run oneid-cli configure')

            if 'SECRET' not in project_admin_credentials:
                raise ValueError('Missing SECRET in credentials, please re-run oneid-cli configure')

            der = base64.b64decode(project_admin_credentials['SECRET'])
            self._keypair = keychain.Keypair.from_secret_der(der)
            self._keypair.identity = project_admin_credentials.get('ID')

            if 'RETURN_KEY' in project_admin_credentials:
                der = base64.b64decode(project_admin_credentials['RETURN_KEY'])
                self._return_keypair = keychain.Keypair.from_public_der(der)

    def get_keypair(self):
        """
        Get the oneID Keypair associated with the current user

        :return: oneid.keychain.Keypair
        """
        if self._keypair is None:
            self._load_project_admin_settings()

        return self._keypair

    def make_api_call(self, endpoint, http_method, **kwargs):
        """
        Make an API HTTP request to oneID

        :param endpoint: URL (all http methods are POST)
        :param kwargs: HTTP method is json, kwargs will be converted to json body
        :return: Response of request
        :raises TypeError: If the kwargs are None, json dumps will fail
        """
        if endpoint[0] == '/':
            endpoint = self.base_url + endpoint

        nonce = kwargs.get('jti', nonces.make_nonce())
        auth_header_token = self._make_auth_header_token(nonce)

        headers = {
            'Content-Type': 'application/jwt',
            'Authorization': 'Bearer %s' % auth_header_token
        }
        data = None

        if http_method in ['POST', 'PUT', 'PATCH']:
            data = self._make_data_jws(kwargs)

        logger.debug('http_method=%s, endpoint=%s, headers=%s, data=%s', http_method, endpoint, headers, data)
        response = requests.request(http_method, endpoint, headers=headers, data=data)

        if response.status_code not in [200, 201]:
            logger.debug('response.status_code=%d', response.status_code)
            raise HTTPException

        mime_type = response.headers.get('Content-Type')
        logger.debug('mime_type=%s', mime_type)
        logger.debug('response.text=%s', response.text)

        if re.match(r'application/(jwt|JOSE(\+JSON))(; charset=utf-8)?', mime_type):
            logger.debug('response.text=%s', response.text)
            message = self._verify_jws_response(response)
            if message.get('jti') != nonce:
                logger.warning('Invalid nonce returned with response')
                raise HTTPException
            return message
        else:
            return response.json()

    def _make_auth_header_token(self, nonce):
        return jwts.make_jwt({
            'jti': nonce,
            'iss': self.keypair.identity
        }, self.keypair)

    def _make_data_jws(self, kwargs):
        return jwts.make_jwt(kwargs, self.keypair)

    def _verify_jws_response(self, response):
        return jwts.verify_jws(response.text, self.return_keypair)


class SelfSignedSession(CLISession):
    """
    A self-signed Session is used for calls like POST /project_admins that
    require that the JWS be signed by a key that in included in the request
    and that returns a response signed by a key that is included in the response
    """

    def __init__(self, keypair, entity_type='project_admin', *args, **kwargs):

        if not keypair:
            raise ValueError('keypair is required')

        super(SelfSignedSession, self).__init__(*args, **kwargs)

        self._keypair = keypair
        self._entity_type = entity_type

    def _load_project_admin_settings(self):
        raise RuntimeError('admin settings should not be loaded from config')

    def _make_auth_header_token(self, nonce):
        return jwts.make_jwt({
            'jti': nonce,
            'iss': self.keypair.identity,
            'public_key': base64.b64encode(self.keypair.public_key_der).decode('utf-8'),
        }, self.keypair)

    def _verify_jws_response(self, response):
        if jose.is_compact_jws(response.text):
            payload = response.text.split('.')[1]
        else:
            payload = response.json()['payload']

        claims = json.loads(utils.base64url_decode(payload).decode('utf-8'))
        lookup = ''.join(word.capitalize() for word in self._entity_type.split('_')) + 's'

        logger.debug('claims=%s, lookup=%s', claims, lookup)

        pa = claims.get(lookup, claims)

        public_keys = pa.get('public_keys')
        logger.debug('public_keys=%s', public_keys)

        return_keypair = keychain.Keypair.from_public_der(base64.b64decode(public_keys[self._entity_type + '_return']))
        return_keypair.identity = pa.get('id')

        return jwts.verify_jws(response.text, return_keypair)
