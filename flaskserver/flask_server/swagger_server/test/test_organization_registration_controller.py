# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.register_org_info_body import RegisterOrgInfoBody  # noqa: E501
from swagger_server.models.settings import Settings  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOrganizationRegistrationController(BaseTestCase):
    """OrganizationRegistrationController integration test stubs"""

    def test_get_org_info(self):
        """Test case for get_org_info

        Register a new organization
        """
        body = RegisterOrgInfoBody()
        response = self.client.open(
            '/api/register/org_info',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_mem_info(self):
        """Test case for post_mem_info

        Upload Database of Employees in a file.
        """
        data = dict(database_file='database_file_example')
        response = self.client.open(
            '/api/register/mem_info',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_post_settings(self):
        """Test case for post_settings

        Select Settings for attendance management.
        """
        body = Settings()
        response = self.client.open(
            '/api/register/settings',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
