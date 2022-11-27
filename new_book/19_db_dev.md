## 数据库操作封装

数据库的SQL 语句大体可以分两类：

* 执行SQL： 例如 插入、删除、更新，这类操作一会返回数据。

* 查询SQL: 查询SQL一般会返回查询的数据，再细分一下又分为：查询单条数据和查询多条数据。


## 封装MySQL执行和查询


__功能代码__

实现MySQL语句的执行和查询方法

```python
# db_api/mysql_db.py
from typing import Any
import pymysql.cursors


class MySQLDB:
    """MySQL DB API"""

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """
        连接 MySQL DB
        :param host: 地址
        :param port: 端口
        :param user: 用户名
        :param password: 密码
        :param database: 数据库名
        """
        self.connection = pymysql.connect(host=host,
                                          port=int(port),
                                          user=user,
                                          password=password,
                                          database=database,
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def execute_sql(self, sql: str) -> None:
        """
        执行 SQL 语句
        """
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
        self.connection.commit()

    def query_sql(self, sql: str) -> list:
        """
        查询 SQL 语句
        return: query data
        """
        data_list = []
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                data_list.append(row)
            self.connection.commit()
            return data_list

    def query_one(self, sql: str) -> Any:
        """
        Query one data SQL
        :return:
        """
        with self.connection.cursor() as cursor:
            self.connection.ping(reconnect=True)
            cursor.execute(sql)
            row = cursor.fetchone()
            self.connection.commit()
            return row

```


__代码说明__

实现MySQLDB 类，在 `__init__()` 初始化方法中接收连接数据库的操作。

实现`execute_sql()` 方法用于执行SQL语句； 

实现 `query_sql()` 用于执行查询SQL语句，其中通过`fetchall()` 方法返回查询结果为列表，如果查询结果为空 返回空列表 []。

实现 `query_one()` 用于执行查询SQL语句，其中通过`fetchone()` 返回一条数据，如果多条结果满足条件，只返回满足条件的第一条数据；结果没有一条数据满足条件返回 None。


__使用例子__

编写测试用例，验证`MySQLDB` 类实现的方法是否可用。

```py
# test_mysql_api.py
import unittest
from db_api.mysql_db import MySQLDB


class MySQLTest(unittest.TestCase):
    """测试操作MySQL数据库API"""

    def setUp(self) -> None:
        """"初始化DB连接"""
        self.db = MySQLDB(host="localhost", port=3306, user="root", password="abc123", database="test_db")

    def test_execute_sql(self):
        """测试执行SQL"""
        db = self.db
        db.execute_sql("INSERT INTO api_user (name, age) VALUES ('tom', 22) ")
        db.execute_sql("UPDATE api_user SET age=23 WHERE name='tom'")
        db.execute_sql("DELETE FROM api_user WHERE name = 'tom' ")
        result = db.query_sql("select * from api_user WHERE name='tom'")
        self.assertEqual(len(result), 0)

    def test_query_sql(self):
        """测试查询SQL"""
        result = self.db.query_sql("select * from api_user")
        self.assertIsInstance(result, list)

    def test_query_one(self):
        """测试查询SQL一条数据"""
        result1 = self.db.query_one("select * from api_user")
        result2 = self.db.query_one("select * from api_user where id=99999")
        self.assertIsInstance(result1, dict)
        self.assertIsNone(result2)

```

__执行结果__

```
❯ python .\test_mysql_api.py
...
----------------------------------------------------------------------
Ran 3 tests in 0.029s

OK
```

## 封装增删查改


通过上面的例子可以看到我们简化 MySQL 连接和操作。但是，还是需要写SQL语句的。例如下面的插入SQL语句，当字段非常多的时候，写起来就比较痛苦了，因为比较难将字段名和字段值做到一一对应。

```sql
INSERT INTO
  table_name (
    `id`,
    `creator`,
    `reviser`,
    `createTime`,
    `shippingFee`,
    `totalAmount`,
    `sumProductPayment`,
    `currency`,
    `toFullName`,
    `toAddress`,
    `toFullAddress`,
    `storageName`,
    `orderTime`,
    `isSplit`,
    `packageNum`,
    `stockOutCreateTime`,
    `stockOutToFullName`,
    `stockOutToFullAddress`,
    `creatorName`,
    `stockOutId`,
    `orderId`
  )
VALUES(
    146,
    9002257,
    9002257,
    "2021-12-05 17:16:55",
    0,
    629,
    629,
    "RMB",
    "张德天",
    "湖北省武汉市",
    "湖北省武汉市洪山区街道口",
    "初始仓库",
    "2021-12-05 17:16:55",
    0,
    "1/1",
    "2021-12-05 17:16:56",
    "张德天",
    "湖北省武汉市洪山区街道口",
    "监狱账号联系人",
    "1467422726779043840",
    "1467422722362441728"
  )

```

那么是否可以像定义字典一样，定义插入的字段名和字段值，例如：

```json
{ 
  "id": 146,
  "creator": 9002257,
  "reviser": 9002257,
  "createTime": "2021-12-05 17:16:55",
  "shippingFee": 0,
  "totalAmount": 629,
  "sumProductPayment": 629,
  "currency": "RMB",
  "toFullName": "张德天",
  "toAddress": "湖北省武汉市",
  "toFullAddress": "湖北省武汉市洪山区街道口",
  "storageName": "初始仓库",
  "orderTime": "2021-12-05 17:16:55",
  "isSplit": 0,
  "packageNum": "1/1",
  "stockOutCreateTime": "2021-12-05 17:16:56",
  "stockOutToFullName": "张德天",
  "stockOutToFullAddress": "湖北省武汉市洪山区街道口",
  "creatorName": "监狱账号联系人",
  "stockOutId": "1467422726779043840",
  "orderId": "1467422722362441728"
}
```

基于这样的需求，我们可以进一步设计一套方法来实现数据的曾/删/查/改。


__功能代码__

实现MySQL语句的执行和查询方法

```python
# db_api/mysql_db.py
from typing import Any
import pymysql.cursors


class SQLBase:
    """SQL base API"""

    @staticmethod
    def dict_to_str(data: dict) -> str:
        """
        dict to set str
        """
        tmp_list = []
        for key, value in data.items():
            if value is None:
                tmp = f"{key}=null"
            elif isinstance(value, int):
                tmp = f"{key}={value}"
            else:
                tmp = f"{key}='{value}'"
            tmp_list.append(tmp)
        return ','.join(tmp_list)

    @staticmethod
    def dict_to_str_and(conditions: dict) -> str:
        """
        dict to where and str
        """
        tmp_list = []
        for key, value in conditions.items():
            if value is None:
                tmp = f"{key}=null"
            elif isinstance(value, int):
                tmp = f"{key}={value}"
            else:
                tmp = f"{key}='{value}'"
            tmp_list.append(tmp)
        return ' and '.join(tmp_list)


class MySQLDB(SQLBase):
    """MySQL DB API"""

    def __init__(self, host: str, port: int, user: str, password: str, database: str) -> None:
        ...

    def execute_sql(self, sql: str) -> None:
        ...

    def query_sql(self, sql: str) -> list:
        ...

    def query_one(self, sql: str) -> Any:
        ...

    def insert(self, table: str, data: dict) -> None:
        """
        插入数据
        :param table: 表名
        :param data: 数据
        """
        for key in data:
            data[key] = "'" + str(data[key]) + "'"
        key = ','.join(data.keys())
        value = ','.join(data.values())
        sql = f"""insert into {table} ({key}) values ({value})"""
        self.execute_sql(sql)

    def select(self, table: str, where: dict = None, one: bool = False) -> Any:
        """
        查询数据
        :param table: 表名
        :param where: 条件
        :param one: 是否返回一条数据
        """
        sql = f"""select * from {table} """
        if where is not None:
            sql += f""" where {self.dict_to_str_and(where)}"""
        if one is True:
            return self.query_one(sql)

        return self.query_sql(sql)

    def update(self, table: str, data: dict, where: dict) -> None:
        """
        更新数据
        :param table: 表名
        :param data: 更新字段
        :param where: 查询条件
        """
        sql = f"""update {table} set """
        sql += self.dict_to_str(data)
        if where:
            sql += f""" where {self.dict_to_str_and(where)};"""
        self.execute_sql(sql)

    def delete(self, table: str, where: dict = None) -> None:
        """
        删除数据
        :param table: 表名
        :param where: 查询条件
        """
        sql = f"""delete from {table}"""
        if where is not None:
            sql += f""" where {self.dict_to_str_and(where)};"""
        self.execute_sql(sql)

```


__代码说明__

注：前面功能中已经实现的方法，在这个功能中用 ... 表示。

首先看`SQLBase` 父类中实现的功能。

* `dict_to_str()`：将字典转换为字符串，并用逗号（,）分割。 例如 `{"id": 1, "name": "tome"}` 转换为 "id=1, name=tom"。 在更新SQL语句中需要用到这样的字符串。

* `dict_to_str_and()`: 将字典转为字符串，并用 and 分割。例如 `{"id": 1, "name": "tome"}` 转换为 "id=1 and name=tom"。 在SQL语句的 where 条件中需要用到这样的字符串。


然后，修改 MySQLDB类继承SQLBase类。

* `insert()`: 插入SQL语句，table 指定表名，data 指定插入的数据。

* `select()`: 查询SQL语句，table 指定表名，where 指定查询的条件，one指定是否返回单条数据。

* `update()`: 更新SQL语句，table 指定表名，data 更新的数据，where 指定查询的条件。

* `delete()`: 删除SQL语句，table 指定表名，where 指定查询的条件。

__使用用例__

编写测试用例，验证`MySQLDB` 类实现的曾/删/查/改方法是否可用。


```py

import unittest
from db_api.mysql_db import MySQLDB


class MySQLTest(unittest.TestCase):
    """测试操作MySQL数据库API"""

    def setUp(self) -> None:
        """"初始化DB连接"""
        self.db = MySQLDB(host="localhost", port=3306, user="root", password="198876", database="guest3")
        self.db.execute_sql("INSERT INTO api_user (name, age) VALUES ('test', 11) ")

    def tearDown(self) -> None:
        self.db.delete("api_user", {"name": "test"})

    def test_select_sql(self):
        """测试查询SQL"""
        result1 = self.db.select(table="api_user", where={"name": "test"})
        self.assertEqual(result1[0]["name"], "test")
        result2 = self.db.select(table="api_user", one=True)
        self.assertIsInstance(result2, dict)

    def test_delete_sql(self):
        """测试删除SQL"""
        # delete sql
        self.db.delete(table="api_user", where={"name": "test"})
        result = self.db.query_sql("select * from api_user WHERE name='test'")
        self.assertEqual(len(result), 0)

    def test_update_sql(self):
        """测试更新SQL"""
        self.db.update(table="api_user", where={"name": "test"}, data={"age": "22"})
        result = self.db.query_sql("select * from api_user WHERE name='test'")
        self.assertEqual(result[0]["age"], 22)

    def test_insert_sql(self):
        """测试插入SQL"""
        self.db.insert(table="api_user", data={"name": "jean", "age": 11})
        result = self.db.query_sql("select * from api_user WHERE name='jean'")
        self.assertTrue(len(result[0]) > 1)

```

使用封装的`select()/delete()/update()/insert()` 等方法使数据库操作变得更加有趣。但是这些方法并不支持复杂的SQL语句，例如联表查询；所以，设计他的目标并不使为了替换SQL语句，只是为了解决简单的SQL操作；如果遇到的复杂的SQL语句，请直接使用 `execute_sql()`，`query_sql()` 等方法。

如果你的项目中要用到其他数据库，同样可以根据MySQLDB类的设计思路去封装相应的数据库的API。
