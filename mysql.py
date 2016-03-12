#!/usr/bin/python
# -*- coding: UTF-8 -*-

import pymysql.cursors


# Connect to the database
connection = pymysql.connect(host='yayayouji.com',
                             user='remote_oceancx',
                             password='Wf6796503.',
                             db='music',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


try:
    with connection.cursor() as cursor:
        # Create a new record
        sql = "INSERT INTO `songs` (`name`, `xiami_id`) VALUES (%s, %s)"
        cursor.execute(sql, ('Jar Of Love', '1770885848'))

    # connection is not autocommit by default. So you must commit to save
    # your changes.
    connection.commit()

    with connection.cursor() as cursor:
        # Read a single record
        sql = "SELECT `id`, `name` FROM `songs` WHERE `xiami_id`=%s"
        cursor.execute(sql, ('1770885848'))
        result = cursor.fetchone()
        print(result)
finally:
    connection.close()