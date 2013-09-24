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

import functools

from tempest import clients
from tempest.common.utils import data_utils
from tempest import exceptions as exc
from tempest import test


def creates(resource):
    """Decorator that adds resources to the appropriate cleanup list."""

    def decorator(f):
        @functools.wraps(f)
        def wrapper(cls, **kwargs):
            result = f(cls, **kwargs)
            body = result[resource]

            if 'uuid' in body:
                cls.created_objects[resource].add(body['uuid'])

            return result
        return wrapper
    return decorator


def check_responce(expected_code):
    """Decorator that checks responce code."""
    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)
            status_code = result['responce']['status']
            expected = str(expected_code)

            if not kwargs.get('expect_errors', False):
                if status_code != expected:
                    raise exc.UnexcpectedResponceCode(expected=expected,
                                                      received=status_code)

            return result
        return wrapper
    return decorator


class BaseBaremetalTest(test.BaseTestCase):
    """Base class for Baremetal API tests."""

    @classmethod
    def setUpClass(cls):
        super(BaseBaremetalTest, cls).setUpClass()

        mgr = clients.Manager()
        cls.client = mgr.baremetal_client

        cls.created_objects = {'chassis': set([]),
                               'port': set([]),
                               'node': set([])}

    @classmethod
    def tearDownClass(cls):
        """Ensure that all created objects get destroyed."""

        super(BaseBaremetalTest, cls).tearDownClass()

        for resource, uuids in cls.created_objects.iteritems():
            delete_method = getattr(cls.client, 'delete_%s' % resource)
            for u in uuids:
                delete_method(u)

    @classmethod
    @creates('chassis')
    @check_responce(200)
    def create_chassis(cls, description=None, expect_errors=False):
        """
        Wrapper utility for creating test chassis.

        :param description: A desctiption of the chassis. if not supplied,
            a random value will be generated.
        :return: Created chassis.

        """
        description = description or data_utils.rand_name('test-chassis-')
        resp, body = cls.client.create_chassis(description=description)

        return {'chassis': body, 'responce': resp}

    @classmethod
    @creates('node')
    @check_responce(200)
    def create_node(cls, cpu_arch='x86', cpu_num=8, storage=1024, memory=4096):
        """
        Wrapper utility for creating test baremetal nodes.

        :param cpu_arch: CPU architecture of the node. Default: x86.
        :param cpu_num: Number of CPUs. Default: 8.
        :param storage: Disk size. Default: 1024.
        :param memory: Available RAM. Default: 4096.
        :return: Created node.

        """
        resp, body = cls.client.create_node(cpu_arch=cpu_arch, cpu_num=cpu_num,
                                            storage=storage, memory=memory)

        # TODO(romcheg): Check the responce to detect errors.
        return {'node': body, 'responce': resp}

    @classmethod
    @creates('port')
    @check_responce(200)
    def create_port(cls, address=None):
        """
        Wrapper utility for creating test ports.

        :param address: MAC address of the port. If not supplied, a random
            value will be generated.
        :return: Created port.

        """
        address = address or data_utils.rand_mac_address()
        resp, body = cls.client.create_port(address=address)

        #TODO(romcheg): Check responce to detect errors.
        return {'port': body, 'responce': resp}
