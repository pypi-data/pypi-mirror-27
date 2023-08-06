# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from .base import KeyManagerType, KeyManagerSubType, BaseKeyManager
from .legacy import LegacyKeyManager
from .ntdi import NTDIPEMKeyManager, NTDIJWKKeyManager


def get_key_manager(typ=None, subtyp=None):

    if typ == KeyManagerType.LEGACY or typ is None:
        return LegacyKeyManager()

    elif typ == KeyManagerType.NTDI:

        if subtyp == KeyManagerSubType.PEM or subtyp is None:
            return NTDIPEMKeyManager()

        elif subtyp == KeyManagerSubType.JWK:
            return NTDIJWKKeyManager()

        else:
            raise ValueError('invalid NTDI KeyManagerSubType: {}'.format(subtyp))

    else:
        raise ValueError('invalid KeyManagerType: {}'.format(typ))


__all__ = [get_key_manager, KeyManagerType, KeyManagerSubType, BaseKeyManager]
