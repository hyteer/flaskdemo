import pymysql.cursors

# Connect to the database
connection = pymysql.connect(host='192.168.198.128',
                             user='tester',
                             password='111',
                             db='BucketList',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

''' First PyMysql sample
try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `tbl_user` (`user_name`, `email`, " \
              "`user_password`) VALUES (%s, %s, %s)"
        cursor.execute(sql, ('silly', 'sillysir@qq.com', '111'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `user_id`, `user_name` FROM `tbl_user` WHERE `email`=%s"
        cursor.execute(sql, ('sillysir@qq.com',))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()
'''




