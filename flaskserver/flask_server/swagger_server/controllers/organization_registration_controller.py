import connexion
import json
import hashlib
import os
from werkzeug.utils import secure_filename

from swagger_server.models.register_org_info_body import RegisterOrgInfoBody  # noqa: E501
from swagger_server.models.settings import Settings  # noqa: E501
from swagger_server import util,db
from flask import make_response


def get_org_info(body=None):  # post info about new organization being registered.
    """Register a new organization

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    # if the request body is in json then only the functions returns a response.
    if connexion.request.is_json:
        # body is stored in a class in RegisterOrgInfoBody.
        body = RegisterOrgInfoBody.from_dict(connexion.request.get_json())
        # a result is searched by unique primary key of organization_table.
        result  = db.get_org_from_id(body.organization_id)
        # if there is already a organization with the organization_id then the status code of 409 is given.
        if result == 1 :
            response_body = {'message': 'Organisation id already taken'}
            status_code = 409
            response_content_type = 'application/json'
        # status code 400 given when the input is invalid i.e. the password and confirm_password do not match.
        elif body.password != body.confirm_password :
            response_body = {'message': 'Given passwords do not match'}
            status_code = 400
            response_content_type = 'application/json'
        # else a new organization can be added to the database.
        else:
            response_body = {'message': 'Data Uploaded Succesfully'}
            status_code = 200
            response_content_type = 'application/json'
            with db.connection.cursor() as cursor:
                # the password is hashed before storage.
                hashed_password = hashlib.sha256(body.password.encode()).hexdigest()
                sql = f"INSERT INTO `organization`(`organization_id`,`admin_name`, `password`,`email_id`,`phone_no`,`address`) VALUES" \
                      f"(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (body.organization_id,body.admin_name, hashed_password, body.email_id, body.phone_number,body.address))
                # commiting the code to the mysql connection stores it.
                db.connection.commit()
        response = make_response(json.dumps(response_body), status_code)
        response.headers['Content-Type'] = response_content_type
        # return the response which has been decided.
        return response

import csv

def post_mem_info(database_file,organization_id):

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



def post_settings(body):  # noqa: E501
    """Select Settings for attendance management.

    Select the different days which are working days for your organization and any ML API you wanted # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: None
    """
    return "do some magic"
