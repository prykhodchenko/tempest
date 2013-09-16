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

import json

from tempest.common import rest_client


class BaremetalClientJSON(rest_client.RestClient):

    def __init__(self, config, username, passwd, auth_url, tenant_name=None):
        super(BaremetalClientJSON, self).__init__(config, username, passwd,
                                                  auth_url, tenant_name)
        self.version = '1'
        self.uri_prefix = 'v%s' % self.version

    def _list_request(self, resource):
        uri = '%(prefix)s/%(resource)s' % {'prefix': self.uri_prefix,
                                           'resource': resource}
        resp, body = self.get(uri, self.headers)
        body = json.loads(body)

        return resp, body

    def list_nodes(self):
        return self._list_request('nodes')

    def list_chassis(self):
        return self._list_request('chassis')

    def list_ports(self):
        return self._list_request('ports')
