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
    """Tempest REST client for Ironic JSON API v1."""

    def __init__(self, config, username, password, auth_url, tenant_name=None):
        super(BaremetalClientJSON, self).__init__(config, username, password,
                                                  auth_url, tenant_name)
        self.service = self.config.baremetal.catalog_type
        self.version = '1'
        self.uri_prefix = 'v%s' % self.version

    def _get_uri(self, resource_name, uuid=None):
        """
        Get URI for a specific resource or object.

        :param resource_name: The name of the REST resource, e.g., 'nodes'.
        :param uuid: The unique identifier of an object in UUID format.
        :return: Relative URI for the resource or object.

        """
        return '{pref}/{res}{uuid}'.format(pref=self.uri_prefix,
                                           res=resource_name,
                                           uuid='/%s' % uuid if uuid else '')

    def _make_patch(self, allowed_attributes, serialize=False, **kw):
        """
        Create a JSON patch according to RFC 6902.

        :param allowed_attributes: An iterable object that contains a set of
            allowed attributes for an object.
        :param serialize: Specifies, whether the patch should be serialized to
            a JSON string or returned as a Python object.
        :param **kw: Attributes and new values for them.
        :return: A JSON path that sets values of the specified attributes to
            the new ones.

        """
        patch = [{"path": "/%s" % attr, "value": kw[attr], "op": "replace"}
                 for attr in allowed_attributes
                 if attr in kw]

        if serialize:
            patch = json.dumps(patch)

        return patch

    def _list_request(self, resource_name):
        """
        Get the list of objects of the specified type.

        :param resource_name: The name of the REST resource, e.g., 'nodes'.
        :return: A tuple with the server response and deserialized JSON list of
                 of objects

        """
        uri = self.get_uri(resource_name)

        resp, body = self.get(uri, self.headers)
        body = json.loads(body)

        return resp, body

    def _create_request(self, resource_name, object_dict):
        """
        Create an object of the specified type.

        :param resource_name: The name of the REST resource, e.g., 'nodes'.
        :param object_dict: A Python dict that represents an object of the
                            specified type.
        :return: A tuple with the server response and the deserialized created
                 object.

        """
        body = json.dumps(object_dict)
        uri = self._get_uri(resource_name)

        resp, body = self.post(uri, headers=self.headers, body=body)
        body = json.loads(body)

        return resp, body

    def _delete_request(self, resource_name, uuid):
        """
        Delete specified object.

        :param resource_name: The name of the REST resource, e.g., 'nodes'.
        :param uuid: The unique identifier of an object in UUID format.
        :return: A tuple with the server response and the responce body.

        """
        uri = self._get_uri(resource_name, uuid)

        resp, body = self.delete(uri, self.headers)
        return resp, body

    def _patch_request(self, resource_name, uuid, patch_object):
        """
        Update specified object with JSON-patch.

        :param resource_name: The name of the REST resource, e.g., 'nodes'.
        :param uuid: The unique identifier of an object in UUID format.
        :return: A tuple with the server responce and the serialized patched
                 object.

        """
        uri = self._get_uri(resource_name, uuid)
        body = json.dumps(patch_object)

        resp, body = self.patch(uri, self.headers, body=body)

    def list_nodes(self):
        """List all existing nodes."""
        return self._list_request('nodes')

    def list_chassis(self):
        """List all existing chassis."""
        return self._list_request('chassis')

    def list_ports(self):
        """List all existing ports."""
        return self._list_request('ports')

    def create_node(self, **kwargs):
        """
        Create a baremetal node with the specified parameters.

        :param arch: CPU architecture of the node. Default: x86_64.
        :param cpus: Number of CPUs. Default: 8.
        :param disk: Disk size. Default: 1024.
        :param ram: Available RAM. Default: 4096.
        :return: A tuple with the server response and the created node.

        """
        node = {'arch': kwargs.get('arch', 'x86_64'),
                'cpus': kwargs.get('cpus', 8),
                'disk': kwargs.get('disk', 1024),
                'ram': kwargs.get('ram', 4096)}

        return self._create_request('nodes', node)

    def create_chassis(self, **kwargs):
        """
        Create a chassis with the specified parameters.

        :param description: The description of the chassis.
            Default: test-chassis
        :return: A tuple with the server response and the created chassis.

        """
        chassis = {'description': kwargs.get('description', 'test-chassis')}

        return self._create_request('chassis', chassis)

    def create_port(self, **kwargs):
        """
        Create a port with the specified parameters.

        :param address: MAC address of the port. Default: 01:23:45:67:89:0A
        :return: A tuple with the server response and the created port.

        """
        port = {'address': '01:23:45:67:89:0A'}

        return self._create_request('ports', port)

    def delete_node(self, uuid):
        """
        Deletes a node having the specified UUID.

        :param uuid: The unique identifier of the node.
        :return: A tuple with the server response and the responce body.

        """
        return self._delete_request('nodes', uuid)

    def delete_chassis(self, uuid):
        """
        Deletes a chassis having the specified UUID.

        :param uuid: The unique identifier of the chassis.
        :return: A tuple with the server response and the responce body.

        """
        return self._delete_request('chassis', uuid)

    def delete_port(self, uuid):
        """
        Deletes a port having the specified UUID.

        :param uuid: The unique identifier of the port.
        :return: A tuple with the server response and the responce body.

        """
        return self._delete_request('ports', uuid)

    def update_node(self, uuid, **kwargs):
        """
        Update the specified node.

        :param uuid: The unique identifier of the node.
        :return: A tuple with the server responce and the updated node.

        """
        node_attributes = ('arch', 'cpus', 'disk', 'ram')
        patch = self._make_patch(node_attributes, **kwargs)

        return self._patch_request('nodes', uuid, patch)

    def update_chassis(self, uuid, **kwargs):
        """
        Update the specified chassis.

        :param uuid: The unique identifier of the chassis.
        :return: A tuple with the server responce and the updated chassis.

        """
        chassis_attributes = ('description')
        patch = self._make_patch(chassis_attributes, **kwargs)

        return self._patch_request('chassis', uuid, patch)

    def update_port(self, uuid, **kwargs):
        """
        Update the specified port.

        :param uuid: The unique identifier of the port.
        :return: A tuple with the server responce and the updated port.

        """
        port_attributes = ('address')
        patch = self._make_patch(port_attributes, **kwargs)

        return self._patch_request('ports', uuid, patch)
