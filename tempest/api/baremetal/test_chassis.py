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
from tempest.common.utils import data_utils
from tempest import test


class TestChassis(base.BaseBaremetalTest):
    """Tests for chassis."""

    @test.attr(type='smoke')
    def test_create_chassis(self):
        descr = data_utils.rand_name('test-chassis-')
        ch = self.create_chassis(description=descr)['chassis']

        self.assertEqual(ch['description'], descr)
