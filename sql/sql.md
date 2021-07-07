# 还可以这样操作数据库

<!-- 去曾经有2天造一条测试用例的经历，这一条用例其实就是一堆SQL脚本，大概几十个表，每张表最多有60个字段的样子，你要摸清表之间的关联关系，最终把写好的SQL插入到数据库，然后，Web页面上跑流程，如果SQL造有问题，web页面流程是组走不下去的。早上起来不想去上班的那种，简直是人生的至暗时刻。 -->

我不喜欢写SQL，本着够用就好的原则，从来没花太多时间去学习SQL。但它在我们工作当中占比还蛮高的，不管是后端开发，还是测试，所以，我更喜欢前端开发的工作。

以前用Django开发的时候借助ORM少写的很多SQL，但是，工作当中还是不可避免的要写一些SQL。

那么有没有一种方式既不写SQL语句，也不用ORM，还可以实现对数据库的CURD操作呢？

接下来看看通过seldom是如何对MySQL进行简单操作的。

### 连接MySQL数据库

1. 安装seldom

```shell
> pip installl seldom==2.1.0
```

2. 安装pymysql驱动

```shell
> pip install pymysql
```

3. 链接MySQL数据库

```py
from seldom.db_operation import MySQLDB

db = MySQLDB(host="127.0.0.1", 
             port="3306", 
             user="root", 
             password="123", 
             database="db_name")
```

### 操作方法

* delete_data

删除表数据。

```py
db.delete_data(table="user", where={"id":1})
```

* insert_data

插入一条数据。

```py
data = {'id': 1, 'username': 'admin', 'password': "123"},
db.insert_data(table="user", data=data)
```

* select_data

查询表数据。

```py
result = db.select_data(table="user", where={"id":1, "name": "tom"})
print(result)
```

* update_data

更新表数据。

```py
db.update_data(table="user", data={"name":"new tom"}, where={"name": "tom"})
```


* init_table

批量插入数据，在插入之前先清空表数据。

```py

datas = {
    'table1': [
        {'id': 1, 'name': '红米Pro发布会'},
        {'id': 2, 'name': '可参加人数为0'},
        {'id': 3, 'name': '当前状态为0关闭'},
        {'id': 4, 'name': '发布会已结束'},
        {'id': 5, 'name': '小米5发布会'},
    ],
    'table2': [
        {'id': 1, 'real_name': 'alen'},
        {'id': 2, 'real_name': 'has sign'},
        {'id': 3, 'real_name': 'tom'},
    ]
}

db.init_table(datas)
```

* close

关闭数据库连接。

```py
db.close()
```

是不是觉得数据的操作变得简单了很多，对数据库的增删查改都是以字典的形式设置数据的。调用CURL对应的方法 设置对应的数据即可。

### 小总

你会发现这种封装是非常鸡肋的，一个简单的多表查询都不能实现。之所以封装到seldom当中，使用场景是为了辅助做自动化用的，比如，在测试一个删除接口之后，需要先通过SQL去插入一条数据，或者调用一个创建接口之后，需要把创建的数据从数据库中删除。那么上面提供的功能基本可以满足这样的需求。

上面提供了一个`init_table()`的方法，其实也是为了更方便的批量插入数据。为什么不通过SQL 语句循环插入呢？因为循环插入的数据没有意义，比如，需要id为1的数据，状态是True，比如需要id为2的数据参加人数为0，必须要手动的设置每条数据，从而满足不同的测试场景。


在实现SQL封装的过程中，我们还找到了另外一个库，它对SQL操作的封装也非常有意思。可以实现更复杂的SQL操作。

https://github.com/whiteclover/dbpy









