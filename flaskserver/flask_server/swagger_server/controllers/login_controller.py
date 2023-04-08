import connexion
import json
import hashlib

from swagger_server.models.admin_login_body import AdminLoginBody 
from swagger_server.models.member_login_body import MemberLoginBody 
from swagger_server import util,db
from flask import make_response


# admin login is done by matching the fields stored in AdminLoginBody
def admin_login(body=None):
    if connexion.request.is_json:
        body = AdminLoginBody.from_dict(connexion.request.get_json())
        # find the organization from the unique primary key organization_id
        query = "SELECT * FROM organization WHERE organization_id = %s"
        values = (body.organization_id)
        with db.connection.cursor() as cursor:
            cursor.execute(query, values)
            # the result is fetched .
            result = cursor.fetchone()
            if result:
                # retrieve the hashed password from the database
                hashed_password = result['password']
                # hash the user input password for comparison
                user_hashed_password = hashlib.sha256(body.password.encode()).hexdigest()
                if user_hashed_password == hashed_password:
                    # if the organization has same passwords then the login is successful.
                    response_body = {'message': 'Login successful!'}
                    status_code = 200
                    response_content_type = 'application/json'
                else:
                    # else the login credentials are invalid.
                    response_body = {'message': 'Invalid login credentials.'}
                    status_code = 400
                    response_content_type = 'application/json'
            # invalid login credentials if the organization does not exist.
            else:
                response_body = {'message': 'Invalid login credentials.'}
                status_code = 400
                response_content_type = 'application/json'

            # response is generated and given.
            response = make_response(json.dumps(response_body), status_code)
            response.headers['Content-Type'] = response_content_type
            return response

# member login is done by matching the fields stored in MemberLoginBody
def member_login(body=None):
    if connexion.request.is_json:
        body = MemberLoginBody.from_dict(connexion.request.get_json())
        # find the unique member from the combined key of member and organization.
        query = "SELECT * FROM member WHERE member_id = %s AND org_id = %s"
        values = (body.member_id, body.organization_id)
        with db.connection.cursor() as cursor:
            cursor.execute(query, values)
            result = cursor.fetchone()
            if result:
                # retrieve the hashed password from the database
                hashed_password = result['password']
                # hash the user input password for comparison
                user_hashed_password = hashlib.sha256(body.password.encode()).hexdigest()
                if user_hashed_password == hashed_password:
                    # if the organization has same passwords then the login is successful.
                    response_body = {'message': 'Login successful!'}
                    status_code = 200
                    response_content_type = 'application/json'
                else:
                    # else the login credentials are invalid.
                    response_body = {'message': 'Invalid login credentials.'}
                    status_code = 400
                    response_content_type = 'application/json'
            # invalid login credentials if the organization does not exist.
            else:
                response_body = {'message': 'Invalid login credentials.'}
                status_code = 400
                response_content_type = 'application/json'
            # response is generated and given.
            response = make_response(json.dumps(response_body), status_code)
            response.headers['Content-Type'] = response_content_type
            return response

