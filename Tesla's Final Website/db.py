import pymysql


connection = pymysql.connect(host='localhost',
                             user='root',
                             password='Bhupesh25',
                             database='attendance',
                             cursorclass=pymysql.cursors.DictCursor)

def setup():
  with connection.cursor() as cursor:
      
    cursor.execute("""CREATE TABLE IF NOT EXISTS `organization` (
        `organization_id` varchar(255)  NOT NULL ,
        `admin_name` varchar(255) NOT NULL,
        `password` TEXT NOT NULL,
        `email_id` varchar(255) NOT NULL,
        `address` varchar(255) NOT NULL,
        `phone_no` varchar(20) NOT NULL,
        `working_days` varchar(255) DEFAULT NULL,
        `face_detection` BOOLEAN DEFAULT false ,
        `face_mask_detection` BOOLEAN DEFAULT false,
        PRIMARY KEY (`organization_id`)                 
      )""")
     
    cursor.execute("""CREATE TABLE IF NOT EXISTS `member` (
        `id` int NOT NULL AUTO_INCREMENT,
        `member_id` varchar(255) NOT NULL,
        `org_id` varchar(255) NOT NULL,
        `member_name` varchar(255) NOT NULL,
        `password` TEXT NOT NULL,
        `email_id` varchar(255) NOT NULL,
        `phone_no` varchar(20) NOT NULL,
        `working_hours` int NOT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`org_id`) REFERENCES `organization`(`organization_id`)       
      )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `attendance` (
        `id` int NOT NULL AUTO_INCREMENT,
        `mem_id` int NOT NULL,
        `date` DATE NOT NULL,
        `time_in` TIME NOT NULL,
        `time_out` TIME NOT NULL,
        `time_needed` TIME NOT NULL,
        `attendance_status` bool NOT NULL,
        PRIMARY KEY (`id`),
        UNIQUE KEY(`date`),
        FOREIGN KEY (`mem_id`) REFERENCES `member`(`id`)      
      )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `leaves` (
        `id` int NOT NULL AUTO_INCREMENT,
        `mem_id` int NOT NULL,
        `fr` DATE NOT NULL,
        `to` DATE NULL,
        `approved` BOOLEAN DEFAULT false,
        `declined` BOOLEAN DEFAULT false,
        `reason` varchar(110) DEFAULT NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`mem_id`) REFERENCES `member`(`id`)       
      )""")

    cursor.execute("""CREATE TABLE IF NOT EXISTS `holidays` (
        `id` int NOT NULL AUTO_INCREMENT,
        `org_id` varchar(255) NOT NULL,
        `fr` DATE NOT NULL,
        `to` DATE NULL,
        PRIMARY KEY (`id`),
        FOREIGN KEY (`org_id`) REFERENCES `organization`(`organization_id`)       
      )""")

# def get_org_from_id(org_id : str) -> bool:
#    with connection.cursor() as cursor:
#       sql = """SELECT * from `organization` WHERE `organization_id` = %s"""
#       cursor.execute(sql,(org_id))
#       r  =cursor.fetchone()
#       if r is None:
#          return 0
#       else:
#          return 1
      
# def get_mem_from_org(org_id: str) -> Optional[List[str]]:
#    with connection.cursor() as cursor:
#       sql = """SELECT * from `member` WHERE `org_id` = %s"""
#       cursor.execute(sql,(org_id))
#       r = cursor.fetchall()
#       if not r:
#          return None
#       else:
#          members = []
#          for row in r:
#             member = row['member_id']
#             members.append(member)
#          return members

# import datetime,calendar

# def holiday_list(org_id: str,year:int,month:int):
#     # Get the list of non-working days for the organization
#     with connection.cursor() as cursor:
#         sql = """SELECT non_working_days FROM organization WHERE organization_id = %s"""
#         cursor.execute(sql, (org_id,))
#         result = cursor.fetchone()
#         non_working_days = result['non_working_days'].split(',') if result else []

#     # Get the list of dates for the specified month
#     days_in_month = calendar.monthrange(year, month)[1]
#     dates = [datetime.date(year, month, day) for day in range(1, days_in_month + 1)]

# def update_attendance(member_id: str, org_id: str, year: int, month: int) -> float:
#     # Get the list of non-working days for the organization
#     with connection.cursor() as cursor:
#         sql = """SELECT non_working_days FROM organization WHERE organization_id = %s"""
#         cursor.execute(sql, (org_id,))
#         result = cursor.fetchone()
#         non_working_days = result['non_working_days'].split(',') if result else []

#     # Get the list of dates for the specified month
#     days_in_month = calendar.monthrange(year, month)[1]
#     dates = [datetime.date(year, month, day) for day in range(1, days_in_month + 1)]

#     # Update the attendance status for each date the member was present
#     total_working_days = 0
#     present_days = 0
#     for date in dates:
#         if date.strftime('%A') not in non_working_days:
#             with connection.cursor() as cursor:
#                 sql = """INSERT INTO attendance (mem_id, date, time_in, time_out, time_needed, attendance_status)
#                          VALUES (%s, %s, NULL, NULL, NULL, TRUE)"""
#                 cursor.execute(sql, (member_id, date))
#             total_working_days += 1
#             present_days += 1

#     # Calculate the attendance percentage
#     attendance_percentage = present_days / total_working_days if total_working_days > 0 else 0.0

#     # Update the attendance percentage in the member table
#     with connection.cursor() as cursor:
#         sql = """UPDATE member SET attendance_this_month = %s, attendance_overall = %s WHERE member_id = %s"""
#         cursor.execute(sql, (attendance_percentage, attendance_percentage, member_id))

#     return attendance_percentage

setup()







