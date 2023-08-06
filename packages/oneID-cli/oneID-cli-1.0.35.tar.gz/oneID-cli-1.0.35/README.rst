..  Copyright 2015-2017 Neustar, Inc.  All rights reserved.
    Licensed under the Apache License, Version 2.0 (the "License"). You may not
    use this file except in compliance with the License. A copy of the License
    has been included with this distribution in the LICENSE file.
    This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
    CONDITIONS OF ANY KIND, either express or implied. See the License for the
    specific language governing permissions and limitations under the License.

Neustar Trusted Device identity (TDI) CLI
=========================================

|CIStatus|_

.. |CIStatus| image:: https://circleci.com/gh/Neustar-TDI/cli.svg?style=shield&circle-token=053ccef5cf83b6254701ab381fe9baf58d28670e
.. _CIStatus: https://circleci.com/gh/Neustar-TDI/cli


About
=====

This tool allows you to interact with your Neustar Trusted Device Identity (TDI) deployment from your terminal.
It can be used to create Projects, provision Devices and Servers, and more. This is an open source tool.
We welcome developer input and contributions to continuously improve the Command Line tool and service the community.

Please report bugs and feature requests through the Issues tab. To contact the TDI team, please email HelpIoT@neustar.biz.


License
=======

This project is licensed under the Apache License Version 2.0. For full details, see `LICENSE <https://github.com/Neustar-TDI/cli/blob/master/LICENSE>`_.


Using TDI CLI
=============

Install TDI Command Line Interface

.. code-block:: console

    pip install oneid-cli


Configure your computer (requires your TDI UUID & Secret Key)

.. code-block:: console

    oneid-cli configure


Create a new Project

.. code-block:: console

    oneid-cli create-project --name "My New Project"



List all your Projects

.. code-block:: console

    oneid-cli list-projects



List details for a Project

.. code-block:: console

    oneid-cli list-projects --project <project-uuid>



Provision a new IoT Device

.. code-block:: console

    oneid-cli provision --type edge_device --name "My IoT Device" --project <project-uuid>



Provision a new Server

.. code-block::

    oneid-cli provision --type server --name "My Server" --project <project-uuid>


To send messages between devices and servers, use `oneid-connect`, available at `<http://oneid-connect.readthedocs.org/en/latest/>`_
