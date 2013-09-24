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

from tempest.api.baremetal import base
from tempest import test


class TestNodes(base.BaseBaremetalTest):
    """Tests for baremetal nodes."""

    @test.attr(type='smoke')
    def test_create_node(self):
        params = {"cpu_arch": "x86_64",
                  "cpu_num": "12",
                  "storage": "10240",
                  "memory": "1024"}

        node = self.create_node(**params)['node']

        for key in params:
            self.assertEqual(node['properties'][key], params[key])
