# Copyright 2017 Neustar, Inc.  All rights reserved.
# Licensed under the Apache License, Version 2.0 (the "License"). You may not
# use this file except in compliance with the License. A copy of the License
# has been included with this distribution in the LICENSE file.
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.

from __future__ import print_function

import os
import argparse
import logging

from .services import Provision, ListProjects, CreateProject, Configure, Revoke, Unrevoke, Show
from .session import CLISession
from . import __version__

logger = logging.getLogger(__name__)


def main():
    session = CLISession()
    handler = CLIHandler(session)
    handler.main()


class CLIHandler(object):
    """
    Run service (provision, configure) with provided arguments

    :param session: Session instance for credentials and configuration
    :type session: session.CLISession

    :Example:

    $ oneid-cli configure --dev-id <unique-id>
                          --dev-secret <secret from developer portal>
                          --project <optional project id>
    """
    def __init__(self, session):
        self._command_table = None
        self._argument_table = None
        self._session = session

    def main(self):
        parser = argparse.ArgumentParser(description='Run oneID Services from the command line')
        parser.add_argument('-d', '--debug',
                            choices=['NONE', 'INFO', 'DEBUG', 'WARNING', 'ERROR'],
                            default='NONE',
                            help='Specify level of debug output (default: %(default)s)')
        parser.add_argument('-c', '--config-file',
                            help='Specify a configuration file to use/update')
        parser.add_argument('--version', '-v', action='version', version='%(prog)s {}'.format(__version__))

        subparsers = parser.add_subparsers(title='Commands', dest='service')
        subparsers.required = True

        args = None

        for cmd, handler in self._get_command_table().items():
            subparser = subparsers.add_parser(cmd)
            required_group = subparser.add_argument_group('required arguments')
            handler.set_up_argparser(required_group, True)
            handler.set_up_argparser(subparser, False)

            subparser.set_defaults(handler=handler)
            subparser.set_defaults(parser=subparser)

        try:
            args = parser.parse_args()

            self._set_logging_level(args.debug)
            logger.debug('args=%s', args)

            if args.config_file:
                # TODO: not this hack
                os.environ['NTDI_CREDENTIALS_FILE'] = args.config_file

            args.handler.run(args)

        except (RuntimeError, ValueError) as e:
            logger.debug('Error running Service:', exc_info=True)
            print(e)

        except SystemExit:
            pass  # Service will have described the problem

        except:  # noqa: E422
            if not args:
                raise
            logger.warning('Error running service "%s"', args.service)
            logger.debug('Exception was:', exc_info=True)

    def _get_command_table(self):
        """
        Build a list of arguments from the available commands
        """
        if self._command_table is None:
            # Map the service commands to classes
            self._command_table = {
                'configure': Configure(self._session),
                'list-projects': ListProjects(self._session),
                'create-project': CreateProject(self._session),
                'provision': Provision(self._session),
                'revoke': Revoke(self._session),
                'unrevoke': Unrevoke(self._session),
                'show': Show(self._session),
                # TODO: sign? -- could see for signing firmware update payloads to scp to devices
                #       check sig? -- not as likely, but maybe for checking downloaded data?
            }
        return self._command_table

    def _set_logging_level(self, debug_level):
        level = getattr(logging, debug_level.upper(), 100)
        logging.basicConfig(level=level, format='%(asctime)-15s %(levelname)-8s [%(name)s:%(lineno)s] %(message)s')
