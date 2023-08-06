# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

import os
import os.path
import re
import contextlib
import logging

logger = logging.getLogger(__name__)


def find(default_filename_base, create=False):
    """
    Create the appropriate Loader for the available file.
    If the ONEID_CREDENTIALS_FILE or NTDI_CREDENTIALS_FILE is set, use that file.
    Throw `ValueError` if it doesn't exist, or isn't a file.
    Otherwise, try to determine the available file based on the provided base name.
      If a legacy file is found, convert to the new format, with .json extension
      If no file found, start a YAML version
    """
    from .yaml_loader import YAMLLoader
    from .json_loader import JSONLoader

    filename = os.environ.get('ONEID_CREDENTIALS_FILE', os.environ.get('NTDI_CREDENTIALS_FILE'))

    if filename:
        return _loader_from_environment(filename, create=create)
    elif os.path.isfile(default_filename_base + '.yml'):
        return YAMLLoader(default_filename_base + '.yml')
    elif os.path.isfile(default_filename_base + '.yaml'):
        return YAMLLoader(default_filename_base + '.yaml')
    elif os.path.isfile(default_filename_base + '.json'):
        return JSONLoader(default_filename_base + '.json')
    elif os.path.isfile(default_filename_base):
        return JSONLoader(default_filename_base, migrate=True)
    else:
        # not finding a config file, create it
        filename = default_filename_base + '.yml'
        _touch(filename)
        return YAMLLoader(filename)


def _loader_from_environment(filename, create=False):
    from .legacy_loader import LegacyLoader
    from .yaml_loader import YAMLLoader
    from .json_loader import JSONLoader

    if not os.path.isfile(filename):

        if os.path.exists(filename):
            raise ValueError('Invalid config file: {}'.format(filename))
        elif create:
            _touch(filename)
        else:
            raise ValueError('Missing config file: {}, run configure'.format(filename))

    extension = os.path.splitext(filename)[1][1:]

    if extension in ['yml', 'yaml']:
        return YAMLLoader(filename)
    elif extension == 'json':
        return JSONLoader(filename)
    elif extension == '':
        return LegacyLoader(filename)
    else:
        raise ValueError('unknown config file type: {}', extension)


def _touch(file_path):
    """
    Make sure a file exists before trying to open

    :param file_path: absolute path to file that needs created
    """
    dir_path = os.path.dirname(file_path)

    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    if not os.path.exists(file_path):
        with open(file_path, 'a'):
            os.utime(file_path, None)


class BaseLoader(object):
    """
    Base class for Loaders
    Does most of the heavy lifting, including picking out the appropriate elements to return
    """
    def __init__(self, filename):
        self._filename = filename

    @property
    def filename(self):
        return self._filename

    @contextlib.contextmanager
    def load(self, project_id=None):
        """
        Context manager for reading the stored configuration file
        """
        config = self.load_config()

        if project_id:
            config = config.get('PROJECTS', {}).get(project_id)

        yield config

    @contextlib.contextmanager
    def update(self, project_id=None):
        """
        Context manager for creating or updating the stored configuration file
        """
        self._touch(self.filename)

        config = self.load_config()

        try:
            project_config = config
            if project_id:
                project_config = config.get('PROJECTS', {}).get(project_id, {})

            yield project_config
        except:  # noqa: E422
            logger.debug('Exception in context manager', exc_info=True)
            raise
        finally:
            if project_id:
                if config.get('PROJECTS') is None:
                    config['PROJECTS'] = {}
                config['PROJECTS'][project_id] = project_config

            self.save_config(config)

    def validate(self, config):
        if 'PROJECT_ADMIN' not in config:
            logger.debug('config=%s', config)
            raise ValueError('Missing "PROJECT_ADMIN" in config')

        pa_config = config['PROJECT_ADMIN']

        # fairly basic checks, no need to decode key formats here

        if 'SECRET' not in pa_config:
            raise ValueError('missing PROJECT_ADMIN.SECRET')

        if not re.match(r'^[a-zA-Z0-9+/]{182}(==|[a-zA-Z0-9+/]=|[a-zA-Z0-9+/]{2})$', pa_config['SECRET']):
            logger.debug('SECRET: %s', pa_config['SECRET'])
            raise ValueError('invalid format for PROJECT_ADMIN.SECRET')

        if 'RETURN_KEY' not in pa_config:
            raise ValueError('missing PROJECT_ADMIN.RETURN_KEY')

        if not re.match(r'^[a-zA-Z0-9+/]{122}(==|[a-zA-Z0-9+/]=|[a-zA-Z0-9+/]{2})$', pa_config['RETURN_KEY']):
            logger.debug('RETURN_KEY: %s', pa_config['RETURN_KEY'])
            raise ValueError('invalid format for PROJECT_ADMIN.RETURN_KEY')

        return True

    def load_config(self):
        logger.error('Attempt to call unimplemented Loader')
        raise NotImplementedError

    def save_config(self, config):
        logger.error('Attempt to call unimplemented Loader')
        raise NotImplementedError

    def _touch(self, file_path):
        _touch(file_path)
