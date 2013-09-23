# vim: tabstop=4 shiftwidth=4 softtabstop=4

#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import random

from tempest.common.utils import data_utils
from tempest import test


class BaseBaremetalTest(test.BaseTestCase):
    """Base class for Baremetal API tests."""

    @classmethod
    def setUpClass(cls):
        super(BaseBaremetalTest, cls).setUpClass()
        cls.created_chassis = []
        cls.created_nodes = []
        cls.created_ports = []

    @classmethod
    def tearDownClass(cls):
        """Ensure that all created objects get destroyed."""

        super(BaseBaremetalTest, cls).tearDownClass()
        for chassis_id in cls.created_chassis:
            cls.client.delete_chassis(chassis_id)

        for node_id in cls.created_nodes:
            cls.client.delete_chassis(node_id)

        for port_id in cls.created_ports:
            cls.client.delete_port(port_id)

    @classmethod
    def create_chassis(cls, description=None):
        """
        Wrapper utility for creating test chassis.

        :param description: A desctiption of the chassis. if not supplied,
            a random value will be generated.
        :return: Created chassis.

        """
        description = description or data_utils.rand_name('test-chassis-')
        resp, body = cls.client.create_chassis(description=description)

        # TODO(romcheg): Check the responce to detect errors.
        return body['chassis']

    @classmethod
    def create_node(cls, arch='x86_64', cpus=8, disk=1024, ram=4096):
        """
        Wrapper utility for creating test baremetal nodes.

        :param arch: CPU architecture of the node. Default: x86_64.
        :param cpus: Number of CPUs. Default: 8.
        :param disk: Disk size. Default: 1024.
        :param ram: Available RAM. Default: 4096.
        :return: Created node.

        """
        resp, body = cls.client.create_node(arch=arch, cpus=cpus,
                                            disk=disk, ram=ram)

        # TODO(romcheg): Check the responce to detect errors.
        return body['node']

    @classmethod
    def create_port(cls, address=None):
        """
        Wrapper utility for creating test ports.

        :param address: MAC address of the port. If not supplied, a random
            value will be generated.
        :return: Created port.

        """
        address = address or ':'.join([r"%02x" % random.randint(0x00, 0xff)
                                       for i in range(6)])
        resp, body = cls.client.create_port(address=address)

        #TODO(romcheg): Check responce to detect errors.
        return body['port']
