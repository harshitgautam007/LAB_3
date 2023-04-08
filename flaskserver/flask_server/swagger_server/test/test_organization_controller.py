# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.holidays import Holidays  # noqa: E501
from swagger_server.models.leaves import Leaves  # noqa: E501
from swagger_server.models.member_information import MemberInformation  # noqa: E501
from swagger_server.models.organization_information import OrganizationInformation  # noqa: E501
from swagger_server.models.settings import Settings  # noqa: E501
from swagger_server.test import BaseTestCase


class TestOrganizationController(BaseTestCase):
    """OrganizationController integration test stubs"""

    def test_display_member_list(self):
        """Test case for display_member_list

        Get list of people for an organization
        """
        query_string = [('name', 'name_example')]
        response = self.client.open(
            '/api/org/{organization_id}/member_list'.format(organization_id='organization_id_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_member_info(self):
        """Test case for member_info

        List the information of the member from the database
        """
        response = self.client.open(
            '/api/org/{organization_id}/{member_id}/info'.format(member_id='member_id_example', organization_id='organization_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_organization_details(self):
        """Test case for organization_details

        List the information of the member from the database
        """
        response = self.client.open(
            '/api/org/{organization_id}/overview'.format(organization_id='organization_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_holidays(self):
        """Test case for show_holidays

        Retrieve a list of holidays marked by the organization.
        """
        response = self.client.open(
            '/api/org/{organization_id}/holidays'.format(organization_id='organization_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_leaves(self):
        """Test case for show_leaves

        Retrieve a list of leaves marked for a member by the organization.
        """
        response = self.client.open(
            '/api/org/{organization_id}/{member_id}/leaves'.format(organization_id='organization_id_example', member_id='member_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_show_settings(self):
        """Test case for show_settings

        show Settings for attendance management.
        """
        response = self.client.open(
            '/api/org/{organization_id}/settings'.format(organization_id='organization_id_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_holidays(self):
        """Test case for update_holidays

        Update the list of holidays marked by the organization.
        """
        body = ['2013-10-20']
        response = self.client.open(
            '/api/org/{organization_id}/holidays'.format(organization_id='organization_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_leaves(self):
        """Test case for update_leaves

        Update the list of leaves of a member marked by the organization.
        """
        body = None
        response = self.client.open(
            '/api/org/{organization_id}/{member_id}/leaves'.format(organization_id='organization_id_example', member_id='member_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_mem_info(self):
        """Test case for update_mem_info

        Upload Database of Employees in a file which is the updated information pertaining to them.
        """
        data = dict(database_file='database_file_example')
        response = self.client.open(
            '/api/org/{organization_id}/update_mem'.format(organization_id='organization_id_example'),
            method='PUT',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_settings(self):
        """Test case for update_settings

        Select Settings for attendance management.
        """
        body = Settings()
        response = self.client.open(
            '/api/org/{organization_id}/settings'.format(organization_id='organization_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_uploadimage(self):
        """Test case for uploadimage

        uploads an image
        """
        body = Settings()
        response = self.client.open(
            '/api/org/{organization_id}/{member_id}/attendance'.format(member_id='member_id_example', organization_id='organization_id_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/octet-stream')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
