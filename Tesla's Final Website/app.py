#!/usr/bin/env python3
from flask import Flask,request,render_template,url_for,redirect, session,flash,Response
import hashlib,pymysql,os,cv2,datetime
import numpy as np
import pandas as pd
# import face_recognition
from fileinput import filename

connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Bhupesh25',
                             database='attendance',
                             cursorclass=pymysql.cursors.DictCursor)




def get_org_from_id(org_id : str) -> bool:
   with connection.cursor() as cursor:
      sql = """SELECT * from `organization` WHERE `organization_id` = %s"""
      cursor.execute(sql,(org_id))
      r  =cursor.fetchone()
      if r is None:
         return 0
      else:
         return 1


app=Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "C:\server\static\\files"
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER



app.secret_key = 'your secret key'

@app.route('/')
def welcome():
    return render_template('main.html')

@app.route('/aboutus')
def aboutus():
    return render_template('AboutUs.html')

@app.route('/admin_login',methods= ['GET','POST'])
def admin_login():
    msg = ''
    if request.method == 'POST'and 'organization_id' in request.form and 'password' in request.form:
        org_id =  request.form['organization_id']
        password = request.form['password']
        if org_id != '' and password != '':
            query = "SELECT * FROM organization WHERE organization_id = %s"
            values = (org_id)
            cursor = connection.cursor()
            cursor.execute(query, values)
            # the result is fetched .
            result = cursor.fetchone()
            if result:
                # retrieve the hashed password from the database
                hashed_password = result['password']
                # hash the user input password for comparison
                user_hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user_hashed_password == hashed_password:
                    session['loggedin'] = "org"
                    session['org_id'] = result
                    session['mem_id'] = None
                    return redirect("/org_overview_redirect")
                else:
                    msg = "incorrect password"
            else:
                msg = "No such organization exists"
        else:
            msg = "Required fields have not been filled"      
    return render_template('admin.html',msg = msg)

@app.route('/member_login',methods=['GET','POST'])
def member_login():
    msg = ''
    if request.method == 'POST'and 'org_id' in request.form and 'member_id' in request.form  and 'password' in request.form:
        member_id = request.form['member_id']
        org_id =  request.form['org_id']
        password = request.form['password']
        if org_id != '' and password != '' and member_id != '':
            query = "SELECT * FROM `member` WHERE `member_id` = %s AND `org_id` = %s"
            values = (member_id,org_id)
            cursor = connection.cursor()
            cursor.execute(query, values)
            # the result is fetched .
            result = cursor.fetchone()
            if result:
                # retrieve the hashed password from the database
                hashed_password = result['password']
                # hash the user input password for comparison
                user_hashed_password = hashlib.sha256(password.encode()).hexdigest()
                if user_hashed_password == hashed_password:
                    session['loggedin'] = "mem"
                    session['org_id'] = None
                    session['mem_id'] = result
                    return redirect(url_for('member', member = result['id']))
                else:
                    msg = "incorrect password"
            else:
                msg = "No such member exists"
        else:
            msg = "Required fields have not been filled"      
    return render_template('login.html',msg = msg)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('org_id', None)
    session.pop('mem', None)
    return redirect("/")

@app.route('/reg_org', methods=['GET', 'POST'])
def reg_org():
    msg = ''
    if request.method == 'POST':
        admin_name = request.form['admin_name']
        organization_id = request.form['organization_id']
        password = request.form['password']
        confirm_password = request.form['cpass']
        address = request.form['address']
        email_id = request.form['email']
        phone_number = request.form['phone_number']
        with connection.cursor() as cursor:
            sql = """SELECT * from `organization` WHERE `organization_id` = %s"""
            cursor.execute(sql, (organization_id))
            r = cursor.fetchone()
            # if there is already an organization with the organization_id then the status code of 409 is given.
            if r is not None:
                msg = "Organization name is already in use"
            # status code 400 given when the input is invalid i.e. the password and confirm_password do not match.
            elif len(password) < 8:
                msg = " The password should be at least 8 characters long"
            elif password != confirm_password:
                msg = "The password should match with confirm password field"
            # else a new organization can be added to the database.
            else:
                # the password is hashed before storage.
                hashed_password = hashlib.sha256(password.encode()).hexdigest()
                sql = f"INSERT INTO `organization`(`organization_id`,`admin_name`, `password`,`email_id`,`phone_no`,`address`) VALUES" \
                        f"(%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (organization_id, admin_name, hashed_password, email_id, phone_number, address))
                # commiting the code to the mysql connection stores it.
                connection.commit()
                sql = """SELECT * from `organization` WHERE `organization_id` = %s"""
                cursor.execute(sql, (organization_id))
                r = cursor.fetchone()
                session['loggedin'] = "org"
                session['org_id'] = r
                session['mem_id'] = None
                return render_template('registration2.html')
    return render_template('registration.html', msg=msg)

        
@app.route('/reg_upload',methods = ['GET','POST'])
def reg_upload():
    msg2 = ''
    if request.method == 'POST':
        org_id = session['org_id']['organization_id']
        database_file = request.files['mem_file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], database_file.filename)
          # set the file path
        database_file.save(file_path)
          # save the file
        csvData = pd.read_csv(file_path,names=['member_id','member_name', 'email_id', 'password' , 'phone_no','working_hours'], header=None)
        members = []
        if not database_file.filename.endswith('.csv'):
            msg2 = " File should be of csv format"
        else:
            for row in csvData.iterrows():
                rows = row[1]
                hashed_pass = hashlib.sha256(rows['password'].encode()).hexdigest()
                member = {
                'member_id': rows['member_id'],
                'member_name': rows['member_name'],
                'email_id': rows['email_id'],
                'password': hashed_pass,
                'phone_no': rows['phone_no'],
                'working_hours': rows['working_hours']
                }
                members.append(member)
        with connection.cursor() as cursor:
            for member in members:
                sql = """INSERT INTO `member`(`member_id`, `org_id`, `member_name`, `password`, `email_id`, `phone_no`, `working_hours`)
                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                cursor.execute(sql, (member['member_id'],org_id,member['member_name'],member['password'],member['email_id'],member['phone_no'],member['working_hours']))
            connection.commit()
        msg2 = 'file uploaded succesfully'
    return render_template('registration2.html',msg2 = msg2)
                
@app.route('/reg_settings',methods=['GET','POST'])   
def reg_settings():
    msg = ''
    if request.method == 'POST':
        org_id = session['org_id']['organization_id']
        sunday = request.form.get('sunday')
        monday = request.form.get('monday')
        tuesday = request.form.get('tuesday')
        wednesday = request.form.get('wednesday')
        thursday = request.form.get('thursday')
        friday = request.form.get('friday')
        saturday = request.form.get('saturday')
        fd = request.form.get('fd')
        fmd = request.form.get('fmd')
        if fd is not None:
            fd = True
        else:
            fd = False
        if fmd is not None:
            fmd = True
        else:
            fmd = False
        days = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
        working_days = ""
        for day in days :
            if day is not None:
                working_days += day + ", "
        if working_days == "":
            msg = "No working days selected"
        else:
            working_days = working_days[:-2]
            with connection.cursor() as cursor:
                sql = """UPDATE `organization` SET `working_days` = %s, `face_detection` = %s, `face_mask_detection` = %s WHERE `organization_id` = %s"""
                cursor.execute(sql,(working_days,fd,fmd,org_id))
                connection.commit()
            return render_template('main.html')
    return render_template('registration2.html',msg = msg)

@app.route('/org_overview_redirect')
def org_overview_redirect():
    if 'loggedin' not in session or session['loggedin'] != 'org':
        # If the 'loggedin' key does not exist or its value is not 'org', redirect to the login page
        flash('Please log in as an organization to access this page')
        return redirect('/logout')
    user_info = session['org_id']
    return render_template('organisation_overview.html',leaves = [],login = session['loggedin'], user_info = user_info)


@app.route('/applyh',methods = ['GET','POST'])
def applyh():
    if 'loggedin' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    cursor= connection.cursor()
    result = session['org_id']
    if request.method == 'POST':
        fr = request.form.get('from')
        to = request.form.get('to')
        sql = """INSERT INTO `holidays`(`org_id`, `fr`, `to`)
                VALUES (%s, %s, %s)"""
        cursor.execute(sql,(result['organization_id'],fr,to))
        connection.commit()
    return render_template('organisation_overview.html',user_info = result,leaves = [],login = session['loggedin'])

current_list1 = []

@app.route('/approveh',methods=['GET','POST'])
def approveh():
    if 'loggedin' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    cursor = connection.cursor()
    result = session['org_id']
    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        query = "SELECT * FROM `holidays` WHERE MONTH(fr) = %s AND YEAR(fr) = %s AND org_id = %s"
        cursor.execute(query, (month, year, result['organization_id']))
        leaves1 = cursor.fetchall()
        query = "SELECT * FROM `holidays` WHERE MONTH(`to`) = %s AND YEAR(`to`) = %s AND org_id = %s"
        cursor.execute(query, (month, year, result['organization_id']))
        leaves2 = cursor.fetchall()
        set1 = set(tuple(d.items()) for d in leaves1)
        set2 = set(tuple(d.items()) for d in leaves2)
        union_set = set1.union(set2)
        final_list = [dict(item) for item in union_set]
        global current_list1
        current_list1 = final_list
    return render_template('organisation_overview.html', user_info=result, leaves=final_list, login=session['loggedin'])


@app.route('/adh', methods=['GET', 'POST'])
def adh():
    if 'loggedin' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    cursor = connection.cursor()
    r = session['org_id']
    if request.method == 'POST':
        action = request.form.get('action')
        if action:
            leave_id = action.split('_')[1]
            sql = """SELECT * FROM `holidays` WHERE `id` = %s"""
            cursor.execute(sql, (leave_id,))
            result = cursor.fetchone()
            sql = """DELETE FROM `holidays` WHERE `id` = %s"""
            cursor.execute(sql, (leave_id,))
            connection.commit()
            global current_list1
            current_list1.remove(result)
    return render_template('organisation_overview.html', user_info=r, leaves=current_list1, login=session['loggedin'])

@app.route('/orgas')
def  orgas():
    if session['loggedin'] == "org":
        return render_template('attendance_update1.html')
    
@app.route('/org_upload',methods = ['GET','POST'])
def org_upload():
    msg2 = ''
    if request.method == 'POST':
        org_id = session['org_id']['organization_id']
        database_file = request.files['mem_file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], database_file.filename)
          # set the file path
        database_file.save(file_path)
          # save the file
        csvData = pd.read_csv(file_path,names=['member_id','member_name', 'email_id', 'password' , 'phone_no','working_hours'], header=None)
        members = []
        if not database_file.filename.endswith('.csv'):
            msg2 = " File should be of csv format"
        else:
            for row in csvData.iterrows():
                rows = row[1]
                hashed_pass = hashlib.sha256(rows['password'].encode()).hexdigest()
                member = {
                'member_id': rows['member_id'],
                'member_name': rows['member_name'],
                'email_id': rows['email_id'],
                'password': hashed_pass,
                'phone_no': rows['phone_no'],
                'working_hours': rows['working_hours']
                }
                members.append(member)
            with connection.cursor() as cursor:
                cursor.execute("DELETE from `member`")
                for member in members:
                    sql = """INSERT INTO `member`(`member_id`, `org_id`, `member_name`, `password`, `email_id`, `phone_no`, `working_hours`)
                            VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                    cursor.execute(sql, (member['member_id'],org_id,member['member_name'],member['password'],member['email_id'],member['phone_no'],member['working_hours']))
                connection.commit()
            msg2 = 'file uploaded succesfully'
    return render_template('attendance_update1.html',msg2 = msg2)
                
@app.route('/org_settings',methods=['GET','POST'])   
def org_settings():
    msg = ''
    if request.method == 'POST':
        org_id = session['org_id']['organization_id']
        sunday = request.form.get('sunday')
        monday = request.form.get('monday')
        tuesday = request.form.get('tuesday')
        wednesday = request.form.get('wednesday')
        thursday = request.form.get('thursday')
        friday = request.form.get('friday')
        saturday = request.form.get('saturday')
        fd = request.form.get('fd')
        fmd = request.form.get('fmd')
        if fd is not None:
            fd = True
        else:
            fd = False
        if fmd is not None:
            fmd = True
        else:
            fmd = False
        days = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]
        working_days = ""
        for day in days :
            if day is not None:
                working_days += day + ", "
        if working_days == "":
            msg = "No working days selected"
        else:
            working_days = working_days[:-2]
            with connection.cursor() as cursor:
                sql = """UPDATE `organization` SET `working_days` = %s, `face_detection` = %s, `face_mask_detection` = %s WHERE `organization_id` = %s"""
                cursor.execute(sql,(working_days,fd,fmd,org_id))
                connection.commit()
            return render_template('attendance_update1.html')
    return render_template('attendance_update1.html',msg = msg)

@app.route('/mem_ov')
def  mem_ov():
    if 'loggedin' not in session or session['loggedin'] != 'org':
        # If the 'loggedin' key does not exist or its value is not 'org', redirect to the login page
        flash('Please log in as an organization to access this page')
        return redirect(url_for('login'))
    search_query = request.args.get('search_query')
    if search_query is None:
        search_query = ""
    with connection.cursor() as cursor:
        org_id = session['org_id']['organization_id']
        sql = """SELECT * from `member` WHERE `org_id` = %s"""
        cursor.execute(sql, (org_id))
        result = cursor.fetchall()

        if search_query:
            result = [member for member in result if search_query.lower() in member['member_name'].lower()]
    return render_template('members_list.html',buttons = result,search_query = search_query)


@app.route('/member/<member>')
def member(member):
    if 'loggedin' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    sql = """SELECT * from `member` WHERE `id` = %s"""
    with connection.cursor() as cursor:
        cursor.execute(sql, (member))
        result = cursor.fetchone()
    return render_template('individual_member.html',user_info = result,leaves = [],login = session['loggedin'])

@app.route('/apply/<member>',methods = ['GET','POST'])
def apply(member):
    if 'loggedin' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    sql = """SELECT * from `member` WHERE `id` = %s"""
    cursor= connection.cursor()
    cursor.execute(sql, (member))
    result = cursor.fetchone()
    if request.method == 'POST':
        fr = request.form.get('from')
        to = request.form.get('to')
        reason = request.form.get('reason')
        sql = """INSERT INTO `leaves`(`mem_id`, `fr`, `to`, `approved`, `declined`,`reason`)
                VALUES (%s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql,(member,fr,to,False,False,reason))
        connection.commit()
    return render_template('individual_member.html',user_info = result,leaves = [],login = session['loggedin'])

current_list = []

@app.route('/approve/<member>',methods = ['GET','POST'])
def approve(member):
    if 'loggedin' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    sql = """SELECT * from `member` WHERE `id` = %s"""
    cursor= connection.cursor()
    cursor.execute(sql, (member))
    result = cursor.fetchone()
    if request.method == 'POST':
        month = int(request.form['month'])
        year = int(request.form['year'])
        cursor = connection.cursor()
        query = "SELECT * FROM `leaves` WHERE MONTH(fr) = %s AND YEAR(fr) = %s AND mem_id = %s"
        cursor.execute(query, (month, year,member))
        leaves1 = cursor.fetchall()
        query = "SELECT * FROM `leaves` WHERE MONTH(`to`) = %s AND YEAR(`to`) = %s AND mem_id = %s"
        cursor.execute(query, (month, year,member))
        leaves2 = cursor.fetchall()
        set1 = set(tuple(d.items()) for d in leaves1)
        set2 = set(tuple(d.items()) for d in leaves2)
        union_set = set1.union(set2)
        final_list = [dict(item) for item in union_set]
        global current_list
        current_list = final_list
    return render_template('individual_member.html',user_info = result,leaves = final_list,login = session['loggedin'])


@app.route('/ad/<member>', methods=['GET', 'POST'])
def ad(member):
    if 'loggedin' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('login'))
    sql = """SELECT * from `member` WHERE `id` = %s"""
    cursor= connection.cursor()
    cursor.execute(sql, (member))
    r = cursor.fetchone()
    if request.method == 'POST':
        action = request.form.get('action')
        if action:
            leave_id = action.split('_')[1]
            if action.startswith('approve'):
                sql = """UPDATE `leaves` SET approved = %s , declined = %s WHERE `id` = %s"""
                cursor.execute(sql, (True,False,leave_id))
            elif action.startswith('decline'):
                sql = """UPDATE `leaves` SET approved = %s , declined = %s WHERE `id` = %s"""
                cursor.execute(sql, (False,True,leave_id))
            connection.commit()
    sql = """SELECT * from `leaves` WHERE `id` = %s"""
    cursor.execute(sql, (leave_id))
    result = cursor.fetchone()
    global current_list
    for i in range(0,len(current_list)):
        leave = current_list[i]
        if leave['id'] == result['id']:
            current_list[i] = result
    return render_template('individual_member.html',user_info = r,leaves = current_list,login = session['loggedin'])


# def detect_faces(frame, member_id):
#     # Load the reference image for this member
#     image_path = os.path.join(app.root_path, "static/faces", f"{member_id}.jpg")
#     reference_image = face_recognition.load_image_file(image_path)
#     reference_encoding = face_recognition.face_encodings(reference_image)[0]

#     # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
#     rgb_frame = frame[:, :, ::-1]

#     # Find all the faces and face encodings in the current frame of video
#     face_locations = face_recognition.face_locations(rgb_frame)
#     face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#     # Loop through each face in this frame of video and see if it matches the reference face
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         # Check if the face is a match for the reference face
#         match = face_recognition.compare_faces([reference_encoding], face_encoding)[0]

#         # If a match was found, mark the attendance and store in database
#         if match:
#             now = datetime.now()
#             cursor = connection.cursor()
#             cursor.execute("INSERT INTO attendance (member_id, time) VALUES (%s, %s)", (member_id, now))
#             connection.commit()

#         # Draw a box around the face
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

#     return frame


# @app.route('/ml')
# def ml():
#     # Open the video stream
#     cap = cv2.VideoCapture(0)

#     while True:
#         ret, frame = cap.read()
#         if not ret:
#             break

#         # Get the logged-in member ID from the session
#         member_id = session['mem_id']['id']  # Replace with actual session data

#         # Detect faces in the frame and mark attendance if a match is found
#         frame = detect_faces(frame, member_id)

#         # Convert the frame to JPEG format for streaming
#         ret, jpeg = cv2.imencode('.jpg', frame)
#         frame = jpeg.tobytes()

#         yield (b'--frame\r\n'
#                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#     cap.release()



if __name__ == '__main__':
    app.run(debug = True)
