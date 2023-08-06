# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function

import os
import six
import logging

import oneid

from .base import BaseKeyManager
from ..constants import TDIKeyStructureFlags

logger = logging.getLogger(__name__)


class LegacyKeyManager(BaseKeyManager):

    def save(self, keystore, fleet_id, keypair_list):
        fleetdir = os.path.join(keystore, 'project-' + fleet_id)
        basename = os.path.join(fleetdir, 'project-' + fleet_id)

        for keydata in keypair_list:
            flags = keydata.get('flags')
            filedir = fleetdir

            if (flags & TDIKeyStructureFlags.ROLE_MASK) == TDIKeyStructureFlags.ROLE_F_C:
                filepatt = basename + '-oneid-{}.pem'
            elif (flags & TDIKeyStructureFlags.ROLE_MASK) == TDIKeyStructureFlags.ROLE_F_S:
                filepatt = basename + '-{}.pem'
            elif 'tdi_type' in keydata and 'tdi_id' in keydata:
                tdi_type = keydata['tdi_type']
                device_id = keydata['tdi_id']
                filedir = os.path.join(fleetdir, tdi_type + '-' + device_id)
                filepatt = os.path.join(filedir, tdi_type + '-' + device_id + '-{}.pem')
            else:
                logger.debug('unable to parse keydata: %s', keydata)
                raise ValueError('unable to determine key type')

            if not os.path.exists(filedir):
                os.makedirs(filedir)
                logger.debug('created directory %s', filedir)

            keypair = keydata['keypair']

            with open(filepatt.format('pub'), 'w') as f:
                f.write(keypair.public_key_pem.decode('utf-8'))
                logger.debug('wrote public key to %s', filepatt.format('pub'))

            if keydata.get('skip_private'):
                continue

            try:
                private_pem = keypair.secret_as_pem.decode('utf-8')

                with open(filepatt.format('priv'), 'w') as f:
                    f.write(private_pem)
                    logger.debug('wrote private key to %s', filepatt.format('priv'))

            except (AttributeError, oneid.exceptions.InvalidFormatError):
                logger.debug('trapped exception getting private key', exc_info=True)
                pass

    def show(self, fleet_id, keypair_list, quiet=False):
        if not keypair_list:
            return

        print('\n')

        for keydata in keypair_list:
            name = keydata.get('name')
            name_str = '{} '.format(name) if name else ''

            print('{}Public Key:\n'.format(name_str))
            print(keydata['keypair'].public_key_pem.decode('utf-8'))
            if not quiet:
                six.moves.input('\nSave contents above, hit "Enter" to continue...')

            if keydata.get('skip_private'):
                continue

            try:
                private_pem = keydata['keypair'].secret_as_pem
                print('{}Private Key:\n'.format(name_str))
                print(private_pem.decode('utf-8'))
                print('\nSAVE CONTENTS ABOVE IN A SECURE LOCATION.')
                if not quiet:
                    six.moves.input('Hit "Enter" to continue...')

            except (AttributeError, oneid.exceptions.InvalidFormatError):
                pass
