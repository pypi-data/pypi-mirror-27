# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function

import os
import json
import six
import logging

import oneid

from .base import BaseKeyManager
from ..constants import TDIKeyStructureFlags

logger = logging.getLogger(__name__)


class BaseNTDIKeyManager(BaseKeyManager):

    def load(self, keystore, fleet_id, kid_list=None):
        ret = []

        with open(keystore, 'r+') as f:
            try:
                keystore_data = json.load(f)
            except ValueError:
                return ret

            if not kid_list:
                kid_list = [fleet_id, 'project/{}'.format(fleet_id)]

            ret = self._find_keydata(keystore_data, fleet_id, kid_list)

        return ret

    def save(self, keystore, fleet_id, keypair_list):

        if not os.path.exists(keystore):
            with open(keystore, 'w+') as f:
                f.write('{}')

        with open(keystore, 'r+') as f:
            try:
                keystore_data = json.load(f)
            except ValueError:
                keystore_data = {}
            keystore_data = self._update_keystore(fleet_id, keypair_list, keystore_data)
            f.seek(0)
            f.truncate()
            json.dump(keystore_data, f)

    def show(self, fleet_id, keypair_list, quiet=False):
        if not keypair_list:
            return

        print('\n' + json.dumps(self._update_keystore(fleet_id, keypair_list), indent=2))

        if not quiet:
            six.moves.input('\nSave contents above, hit "Enter" to continue...')

    def _update_keystore(self, fleet_id, keypair_list, keystore=None):
        raise NotImplementedError

    def _kid_from_keydata(self, fleet_id, keydata):
        ret = str(fleet_id)

        if 'tdi_id' in keydata:
            ret = str(keydata['tdi_id'])

        elif (keydata['flags'] & TDIKeyStructureFlags.ROLE_MASK) == TDIKeyStructureFlags.ROLE_F_C:
            ret = 'project/{}'.format(ret)

        elif (keydata['flags'] & TDIKeyStructureFlags.ROLE_MASK) != TDIKeyStructureFlags.ROLE_F_S:
            logger.debug('unable to determine kid from keydata: %s', keydata)
            raise ValueError('unable to determine kid from keydata')

        return ret


class NTDIPEMKeyManager(BaseNTDIKeyManager):

    def _find_keydata(self, keystore, fleet_id, kid_list):
        logger.debug('keystore=%s', keystore)
        ret = []

        for kid in kid_list:
            key = keystore.get(kid, {})

            logger.debug('kid=%s, key=%s', kid, key)

            if key.get('kid') == kid and key.get('fleet') == fleet_id:
                key_ref = key.get('reference', {})

                if 'priv' in key_ref:
                    keypair = oneid.keychain.Keypair.from_secret_pem(key_ref['priv'])
                else:
                    keypair = oneid.keychain.Keypair.from_public_pem(key_ref['pub'])

                ret.append({
                    'keypair': keypair,
                    'flags': key['flags'],
                    'skip_private': False,
                })

        return ret

    def _key_reference(self, keydata):
        keypair = keydata['keypair']
        ret = {
            'pub': keypair.public_key_pem.decode('utf-8'),
        }

        if not keydata['skip_private']:
            try:
                ret['priv'] = keypair.secret_as_pem.decode('utf-8')

            except (AttributeError, oneid.exceptions.InvalidFormatError):
                logger.debug('trapped exception getting private key', exc_info=True)
                pass

        return ret

    def _update_keystore(self, fleet_id, keypair_list, keystore=None):
        logger.debug('updating with %s', keypair_list)
        if not keystore:
            keystore = {}

        for keydata in keypair_list:
            kid = self._kid_from_keydata(fleet_id, keydata)
            logger.debug('kid=%s', kid)

            keystore[kid] = {
                'kid': kid,
                'fleet': str(fleet_id),
                'flags': keydata['flags'],
                'reference': self._key_reference(keydata),
            }

        return keystore


class NTDIJWKKeyManager(BaseNTDIKeyManager):

    def _find_keydata(self, keystore, fleet_id, kid_list):
        logger.debug('fleet_id=%s, kid_list=%s', fleet_id, kid_list)
        return [
            {
                'keypair': oneid.keychain.Keypair.from_jwk(key['ref']),
                'flags': key['flags'],
                'skip_private': False,
            }
            for key in keystore['keys']
            if key['fleet'] == fleet_id and key['kid'] in kid_list
        ]

    def _key_reference(self, keydata):
        keypair = keydata['keypair']
        ret = keypair.jwk

        if 'd' in ret and keydata['skip_private']:
            del ret['d']

        # TODO: remove once these are added in python-sdk
        if 'use' not in ret:  # pragma: no branch
            ret['use'] = 'sig'
            ret['alg'] = 'ES256'

        return ret

    def _update_keystore(self, fleet_id, keypair_list, keystore=None):
        if not keystore:
            keystore = {}

        if 'keys' not in keystore:
            keystore['keys'] = []

        for keydata in keypair_list:
            kid = self._kid_from_keydata(fleet_id, keydata)

            keystore['keys'] = [key for key in keystore['keys'] if key['kid'] != kid] + [{
                'kid': kid,
                'fleet': str(fleet_id),
                'flags': keydata['flags'],
                'ref': self._key_reference(keydata),
            }]

        return keystore
