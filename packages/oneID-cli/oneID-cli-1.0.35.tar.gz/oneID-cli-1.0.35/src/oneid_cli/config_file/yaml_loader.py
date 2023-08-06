# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import logging
import ruamel.yaml as yaml

from .base_loader import BaseLoader

logger = logging.getLogger(__name__)


class YAMLLoader(BaseLoader):
    def load_config(self):
        ret = None
        with open(self.filename, 'rb') as fin:
            ret = yaml.load(fin, Loader=yaml.RoundTripLoader) or {}
        return ret

    def save_config(self, config):
        self.validate(config)
        with open(self.filename, 'w') as fout:
            logger.debug('saving config: %s', config)
            yaml.dump(config, fout, indent=2, Dumper=yaml.RoundTripDumper)
