# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
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
from urlparse import urlparse

from tempest.common.rest_client import RestClient


class CredentialsClientJSON(RestClient):

    def __init__(self, config, username, password, auth_url, tenant_name=None):
        super(CredentialsClientJSON, self).__init__(config, username, password,
                                                    auth_url, tenant_name)
        self.service = self.config.identity.catalog_type
        self.endpoint_url = 'adminURL'

    def request(self, method, url, headers=None, body=None, wait=None):
        """Overriding the existing HTTP request in super class rest_client."""
        self._set_auth()
        self.base_url = self.base_url.replace(urlparse(self.base_url).path,
                                              "/v3")
        return super(CredentialsClientJSON, self).request(method, url,
                                                          headers=headers,
                                                          body=body)

    def create_credential(self, access_key, secret_key, user_id, project_id):
        """Creates a credential."""
        blob = "{\"access\": \"%s\", \"secret\": \"%s\"}" % (
            access_key, secret_key)
        post_body = {
            "blob": blob,
            "project_id": project_id,
            "type": "ec2",
            "user_id": user_id
        }
        post_body = json.dumps({'credential': post_body})
        resp, body = self.post('credentials', post_body,
                               self.headers)
        body = json.loads(body)
        body['credential']['blob'] = json.loads(body['credential']['blob'])
        return resp, body['credential']

    def update_credential(self, credential_id, **kwargs):
        """Updates a credential."""
        resp, body = self.get_credential(credential_id)
        cred_type = kwargs.get('type', body['type'])
        access_key = kwargs.get('access_key', body['blob']['access'])
        secret_key = kwargs.get('secret_key', body['blob']['secret'])
        project_id = kwargs.get('project_id', body['project_id'])
        user_id = kwargs.get('user_id', body['user_id'])
        blob = "{\"access\": \"%s\", \"secret\": \"%s\"}" % (
            access_key, secret_key)
        post_body = {
            "blob": blob,
            "project_id": project_id,
            "type": cred_type,
            "user_id": user_id
        }
        post_body = json.dumps({'credential': post_body})
        resp, body = self.patch('credentials/%s' % credential_id, post_body,
                                self.headers)
        body = json.loads(body)
        body['credential']['blob'] = json.loads(body['credential']['blob'])
        return resp, body['credential']

    def get_credential(self, credential_id):
        """To GET Details of a credential."""
        resp, body = self.get('credentials/%s' % credential_id)
        body = json.loads(body)
        body['credential']['blob'] = json.loads(body['credential']['blob'])
        return resp, body['credential']

    def list_credentials(self):
        """Lists out all the available credentials."""
        resp, body = self.get('credentials')
        body = json.loads(body)
        return resp, body['credentials']

    def delete_credential(self, credential_id):
        """Deletes a credential."""
        resp, body = self.delete('credentials/%s' % credential_id)
        return resp, body
