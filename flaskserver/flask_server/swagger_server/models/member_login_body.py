# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class MemberLoginBody(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, organization_id: str=None, member_id: str=None, password: str=None):  # noqa: E501
        """MemberLoginBody - a model defined in Swagger

        :param organization_id: The organization_id of this MemberLoginBody.  # noqa: E501
        :type organization_id: str
        :param member_id: The member_id of this MemberLoginBody.  # noqa: E501
        :type member_id: str
        :param password: The password of this MemberLoginBody.  # noqa: E501
        :type password: str
        """
        self.swagger_types = {
            'organization_id': str,
            'member_id': str,
            'password': str
        }

        self.attribute_map = {
            'organization_id': 'organization_id',
            'member_id': 'member_id',
            'password': 'password'
        }
        self._organization_id = organization_id
        self._member_id = member_id
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'MemberLoginBody':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The member_login_body of this MemberLoginBody.  # noqa: E501
        :rtype: MemberLoginBody
        """
        return util.deserialize_model(dikt, cls)

    @property
    def organization_id(self) -> str:
        """Gets the organization_id of this MemberLoginBody.


        :return: The organization_id of this MemberLoginBody.
        :rtype: str
        """
        return self._organization_id

    @organization_id.setter
    def organization_id(self, organization_id: str):
        """Sets the organization_id of this MemberLoginBody.


        :param organization_id: The organization_id of this MemberLoginBody.
        :type organization_id: str
        """
        if organization_id is None:
            raise ValueError("Invalid value for `organization_id`, must not be `None`")  # noqa: E501

        self._organization_id = organization_id

    @property
    def member_id(self) -> str:
        """Gets the member_id of this MemberLoginBody.


        :return: The member_id of this MemberLoginBody.
        :rtype: str
        """
        return self._member_id

    @member_id.setter
    def member_id(self, member_id: str):
        """Sets the member_id of this MemberLoginBody.


        :param member_id: The member_id of this MemberLoginBody.
        :type member_id: str
        """
        if member_id is None:
            raise ValueError("Invalid value for `member_id`, must not be `None`")  # noqa: E501

        self._member_id = member_id

    @property
    def password(self) -> str:
        """Gets the password of this MemberLoginBody.


        :return: The password of this MemberLoginBody.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this MemberLoginBody.


        :param password: The password of this MemberLoginBody.
        :type password: str
        """
        if password is None:
            raise ValueError("Invalid value for `password`, must not be `None`")  # noqa: E501

        self._password = password