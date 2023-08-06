# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
import json
import contextlib

from collections import OrderedDict

from .base_loader import BaseLoader


class LegacyLoader(BaseLoader):
    @contextlib.contextmanager
    def load(self, project_id=None):
        """
        Context manager for reading the stored configuration file
        """
        try:
            with open(self.filename, 'r') as credential_file:
                credentials = json.load(credential_file)
                if project_id:
                    credentials = credentials.get(project_id, credentials.get('DEFAULT'))
                else:
                    credentials = {
                        'PROJECT_ADMIN': credentials.get('DEFAULT'),
                        'PROJECTS': credentials,
                    }

                yield credentials
        finally:
            pass

    @contextlib.contextmanager
    def update(self, project_id=None):
        """
        Context manager for creating or updating the stored configuration file
        """
        self._touch(self.filename)

        with open(self.filename, 'r+') as credential_file:
            if os.stat(self.filename).st_size == 0:
                credentials = {}
            else:
                credentials = json.load(credential_file, object_pairs_hook=OrderedDict)
                credentials = {
                    'PROJECT_ADMIN': credentials.get('DEFAULT'),
                    'PROJECTS': credentials,
                }

            return_credentials = credentials
            if project_id:
                return_credentials = credentials.get('PROJECTS').get(project_id, {})

            yield return_credentials

            if project_id:
                credentials[project_id] = return_credentials
            else:
                credentials = return_credentials.get('PROJECTS', {})
                credentials['DEFAULT'] = return_credentials.get('PROJECT_ADMIN', {})
            # seek back to the start of the file
            credential_file.seek(0)
            json.dump(credentials, credential_file, sort_keys=False, indent=4)
            credential_file.truncate()
