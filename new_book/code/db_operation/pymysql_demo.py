import pymysql.cursors

# 连接数据库
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='198876',
                             database='dev4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:

    with connection.cursor() as cursor:
        # 查询auth_user表
        sql = "SELECT `id`, `name`, `email` FROM `user`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
