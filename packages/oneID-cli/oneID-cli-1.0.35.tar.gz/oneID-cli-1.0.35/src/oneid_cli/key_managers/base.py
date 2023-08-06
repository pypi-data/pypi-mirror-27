# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.


class KeyManagerType(object):
    LEGACY = 'legacy'
    NTDI = 'ntdi'


class KeyManagerSubType(object):
    PEM = 'pem'
    JWK = 'jwk'


class BaseKeyManager(object):
    def load(self, keystore, fleet_id, kid_list=None):
        raise NotImplementedError

    def save(self, keystore, fleet_id, keypair_list):
        raise NotImplementedError

    def show(self, fleet_id, keypair_list, quiet=False):
        raise NotImplementedError
