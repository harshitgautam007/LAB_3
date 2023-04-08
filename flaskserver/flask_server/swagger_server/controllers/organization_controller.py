import connexion
import json
import hashlib
import csv

from swagger_server.models.holidays import Holidays  # noqa: E501
from swagger_server.models.leaves import Leaves  # noqa: E501
from swagger_server.models.member_information import MemberInformation  # noqa: E501
from swagger_server.models.organization_information import OrganizationInformation  # noqa: E501
from swagger_server.models.settings import Settings  # noqa: E501
from swagger_server import util,db
from flask import make_response


def display_member_list(organization_id, name: None):
    # Call the `get_org_from_id` function to retrieve the list of members for the specified organization
    member_list = db.get_mem_from_org(organization_id)

    # Check if the organization exists
    if  member_list == None:
        response_body = {'member_list': []}
        status_code = 200
    else:
        # Filter the member list by name if the `name` parameter is provided
        member_list = [m for m in member_list if name.lower() in m.lower()]

        # Return the member list as a JSON response
        response_body = {'member_list': member_list}
        status_code = 200

    # Create the response
    response_content_type = 'application/json'
    response = make_response(json.dumps(response_body), status_code)
    response.headers['Content-Type'] = response_content_type

    return response


def member_info(member_id, organization_id):  # noqa: E501
    # search for unique key using organization_id and member_id of a person.
    sql = """SELECT * from `member` WHERE `org_id` = %s AND `member_id` = %s"""
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id,member_id))
        r = cursor.fetchone()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 404
            response_content_type = 'application/json'
        else:
            response_body = {'member_id': r['member_id'],'member_name': r['member_name'],'org_id': r['org_id'],'email_id': r['email_id']}
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def organization_details(organization_id):  # noqa: E501
    sql = """SELECT * from `organization` WHERE `organization_id` = %s """
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id))
        r = cursor.fetchone()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 404
            response_content_type = 'application/json'
        else:
            response_body = {'phone_no': r['phone_no'],'admin_name': r['admin_name'],'organization_id': r['organization_id'],'email_id': r['email_id']}
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def show_holidays(organization_id):  # noqa: E501
    sql = """SELECT * from `holidays` WHERE `org_id` = %s """
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id))
        r = cursor.fetchall()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 200
            response_content_type = 'application/json'
        else:
            response_body = {'holidays': r['holidays'],'face_detection': r['face_detection'],'face_mask_detection': r['face_mask_detection']}
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def show_leaves(organization_id, member_id):  # noqa: E501
    """Retrieve a list of leaves marked for a member by the organization.

     # noqa: E501

    :param organization_id: ID of the organization to retrieve holidays for.
    :type organization_id: str
    :param member_id: ID of member
    :type member_id: str

    :rtype: Leaves
    """
    sql = """SELECT * from `holidays` WHERE `org_id` = %s """
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id))
        r = cursor.fetchall()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 200
            response_content_type = 'application/json'
        else:
            response_body = {'holidays': r['holidays'],'face_detection': r['face_detection'],'face_mask_detection': r['face_mask_detection']}
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def show_settings(organization_id):  # noqa: E501
    sql = """SELECT * from `organization` WHERE `organization_id` = %s """
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id))
        r = cursor.fetchone()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 200
            response_content_type = 'application/json'
        else:
            response_body = {'holidays' :r['holidays'], 'face_detection': r['face_detection'], 'face_mask_detection': r['face_mask_detection'] }
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def update_holidays(body, organization_id):  # noqa: E501
    """Update the list of holidays marked by the organization.

     # noqa: E501

    :param body: List of holidays to update.
    :type body: List[]
    :param organization_id: ID of the organization to update holidays for.
    :type organization_id: str

    :rtype: None
    """
    sql = """SELECT * from `organization` WHERE `organization_id` = %s """
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id))
        r = cursor.fetchone()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 404
            response_content_type = 'application/json'
        else:
            response_body = {'phone_no': r['phone_no'],'admin_name': r['admin_name'],'organization_id': r['organization_id'],'email_id': r['email_id']}
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def update_leaves(body, organization_id, member_id):  # noqa: E501
    """Update the list of leaves of a member marked by the organization.

     # noqa: E501

    :param body: List of leaves to update.
    :type body: List[]
    :param organization_id: ID of the organization.
    :type organization_id: str
    :param member_id: ID of member.
    :type member_id: str

    :rtype: None
    """
    sql = """SELECT * from `holidays` WHERE `org_id` = %s """
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id))
        r = cursor.fetchall()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 200
            response_content_type = 'application/json'
        else:
            response_body = {'holidays': r['holidays'],'face_detection': r['face_detection'],'face_mask_detection': r['face_mask_detection']}
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def update_mem_info(database_file, organization_id):  # noqa: E501
    """Upload Database of Employees in a file which is the updated information pertaining to them.

    Endpoint for uploading a database file containing details of the employee such as its Employee id,Name,Email ID. # noqa: E501

    :param database_file: 
    :type database_file: strstr
    :param organization_id: organization whose members are updated
    :type organization_id: str

    :rtype: None
    """
    if not database_file.endswith('.csv'):
        response_body = {'message': 'Invalid Request'}
        status_code = 400
        response_content_type = 'application/json'

    try:
        # Open the CSV file and read the contents
        with open(database_file, 'r') as file:
            csv_reader = csv.reader(file)
            employees = []
            for row in csv_reader:
                hashed_pass = hashlib.sha256(row['password'].encode()).hexdigest()
                employee = {
                'member_id': row['Employee id'],
                'member_name': row['Name'],
                'email_id': row['Email ID'],
                'password': hashed_pass,
                'phone_no': row['phone_no'],
                'working_hours': row['phone_no']
                }
                employees.append(employee)
            with db.connection.cursor() as cursor:
                for employee in employees:
                    sql = """INSERT INTO `member` 
                            (`member_id`, `org_id`, `member_name`, `password`, `email_id`, `phone_no`, `working_hours`)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (
                        employee['member_id'],
                        organization_id,
                        employee['member_name'],
                        employee['password'],
                        employee['email_id'],
                        employee['phone_no'],
                        employee['working_hours']
                    ))
                db.connection.commit()
            response_body = {'message': 'Data Uploaded Succesfully'}
            status_code = 201
            response_content_type = 'application/json'
    except:
        response_body = {'message': 'Access Denied'}
        status_code = 403
        response_content_type = 'application/json'
    response = make_response(json.dumps(response_body), status_code)
    response.headers['Content-Type'] = response_content_type
    return response


def update_settings(body, organization_id):  # noqa: E501
    """Select Settings for attendance management.

    Select the different days which are working days for your organization and any ML API you wanted # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param organization_id: organization whose settings are updated
    :type organization_id: str

    :rtype: Settings
    """
    sql = """SELECT * from `holidays` WHERE `org_id` = %s """
    with db.connection.cursor() as cursor:
        cursor.execute(sql,(organization_id))
        r = cursor.fetchall()
        if not r:
            response_body = {'message': 'Not Found.'}
            status_code = 200
            response_content_type = 'application/json'
        else:
            response_body = {'holidays': r['holidays'],'face_detection': r['face_detection'],'face_mask_detection': r['face_mask_detection']}
            status_code = 200
            response_content_type = 'application/json'
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        return response


def uploadimage(member_id, organization_id, body=None):  # noqa: E501
    """uploads an image

    The time and date of the image are also noted. # noqa: E501

    :param member_id: ID of pet to update
    :type member_id: str
    :param organization_id: The ID of the member to retrieve information for
    :type organization_id: str
    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    if connexion.request.is_json:
        body = Settings.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
