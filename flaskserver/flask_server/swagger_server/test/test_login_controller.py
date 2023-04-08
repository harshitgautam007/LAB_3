# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.admin_login_body import AdminLoginBody  # noqa: E501
from swagger_server.models.member_login_body import MemberLoginBody  # noqa: E501
from swagger_server.test import BaseTestCase


class TestLoginController(BaseTestCase):
    """LoginController integration test stubs"""

    def test_admin_login(self):
        """Test case for admin_login

        Login for admin of an organization
        """
        body = AdminLoginBody()
        response = self.client.open(
            '/api/admin_login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_member_login(self):
        """Test case for member_login

        Login for a member of an organization
        """
        body = MemberLoginBody()
        response = self.client.open(
            '/api/member_login',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
