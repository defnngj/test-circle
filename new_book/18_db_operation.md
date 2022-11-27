## 数据库操作

在做自动化的过程中，经常会涉及到数据库的操作，例如，测试数据的准备，数据入库的检查等。既然是一个高频的需求，我们可以将数据库操作集成到测试框架中实现。


## 操作数据库技术

python语言操作数据库可以涉及到两个维度技术。

* 数据库驱动：这个是必要的，例如操作SQLite、MySQL、oracle、Mongodb、`SQL Server`等数据库都需要对应的驱动库。

* ORM: 是 Object Relational Mapping 的缩写，即为`“对象关系映射”`，它解决了对象和关系型数据库之间的数据交互问题。

### 数据库驱动

在编程语言下面，连接每一种数据库都需要对应的驱动。以MySQL数据库为例，我们可以使用pymysql驱动库。

* pip安装pymysql

```shell
> pip install pymysql
```

我们通常使用数据库客户端操作数据库。例如: SQLyog

![](./img/mysql_client.png)

通过pymysql通过可以连接和操作数据库。

__功能代码__

```py
# pymysql_demo.py
import pymysql.cursors

# 连接数据库
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='pawd123',
                             database='dev4',
                             cursorclass=pymysql.cursors.DictCursor)

with connection:

    with connection.cursor() as cursor:
        # 查询auth_user表
        sql = "SELECT `id`, `name`, `email` FROM `user`"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
```

__代码说明:__

* `pymysql.connect()`: 建立MySQL数据库连接，需要填写地址（host）、用户名（user）、密码（password）、数据库（database）等；不同的数据库连接方式也会有所不同，例如SQLite数据库只需要指定数据库文件路径即可。

* `cursor()`: 建立数据库光标。

* `execute()`: 用于执行SQL语句。

* `fetchone()`: 用户查询一条数据，返回dict格式的数据；也可以使用`fetchall()` 用于查询所有数据，返回list格式的数据。


__查询结果__

```
{'id': 1, 'name': 'admin', 'email': 'admin@gmail.com'}
```


### ORM

ORM可以看作是基于数据库驱动更高一级的封装，不在使用SQL语句，通过编程语言的概念对数据库进行操作。以sqlalchemy为例。

* pip 安装 sqlalchemy

```
> pip install sqlalchemy
```

__功能代码__

```py
# pymysql_demo.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy.types import *
from sqlalchemy.orm import sessionmaker


# 数据库连接
engine = create_engine("mysql+pymysql://root:pawd123@localhost/dev_db", encoding='utf-8')
Session = sessionmaker(bind=engine)
s = Session()

Base = declarative_base()

class User(Base):
    """user表对象"""
    __tablename__ = 'user'  # 表名

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    password = Column(String(100))
    email = Column(String(100))

    def __repr__(self):
        return "<id:%s name:%s email:%s>" % (self.id, self.name, self.email)

# 查询user表
user = s.query(User).filter(User.name == 'admin').first()
print(f"id: {user.id}, name:{user.name}, email:{user.email}")

```

__代码说明:__

* `create_engine()`: 建立MySQL数据库连接，需要填写地址（host）、用户名（user）、密码（password）、数据库（database）等.

* `sessionmaker()`: 创建session绑定数据库引擎。

* `User类`: 创建User类与数据库user表对应关系。

* `query()`: 查询查询User表，通过`filter()`指定查询条件，`first()`返回第一条数据。

__查询结果__

```
id:1, name:admin, email:admin@gmai.com
```


docker run -e "ACCEPT_EULA=Y" -e "MSSQL_SA_PASSWORD=tc@198876" -p 1433:1433 --name sql1 --hostname sql1 -d mcr.microsoft.com/mssql/server:2022-latest


docker exec -it sql1 "bash"

CREATE TABLE `users` (`id` int(11) NOT NULL AUTO_INCREMENT, `email` varchar(255) COLLATE utf8_bin NOT NULL, `password` varchar(255) COLLATE utf8_bin NOT NULL, PRIMARY KEY `id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=1;

```sql
CREATE TABLE users (id INT  NOT NULL IDENTITY(1,1) PRIMARY KEY, email VARCHAR(50)  NOT NULL,  password VARCHAR(30) NOT NULL);
```

