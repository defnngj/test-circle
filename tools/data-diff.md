# data-diff数据工具

![](./image/data-diff-logo.png)

## data-diff 介绍

> 有很多场景我们都需要用到数据对比，比如数据迁移，系统升级重新设计数据库表，那么就需要验证数据一致性。data-diff 是一个非常好用的Python开源工具。

data-diff 在SQL数据库内或跨SQL数据库快速比较数据集。

data-diff 提供两种对比模式

- Joindiff
  - 推荐用于在同一数据库内比较数据
  - 使用外连接操作以尽可能高效地在同一数据库内区分行
  - 完全依赖底层数据库引擎进行计算
  - 需要使用单个SQL查询来查询两个数据集
  - 时间复杂度接近于JOIN操作，并且在数据集中的差异数量上基本独立。
- hashdiff
  - 推荐用于跨不同数据库比较数据集
  - 在同一数据库内，也可帮助区分非常大的表，其中预期的差异很少
  - 采用基于哈希和二分搜索的分治算法
  - 可在不同的数据库引擎之间区分数据，例如 PostgreSQL <> Snowflake
  - 当差异很少时，时间复杂度接近于COUNT(*)操作
  - 当数据集有大量差异时，性能会下降


## 安装

data-diff 通过Python语言开发，使用 pip 安装。
- 安装data-diff

```shell
pip install data-diff
```

- 安装数据库依赖

```shell
pip install 'data_diff[mysql]'
```

data-diff 支持多种数据库，我们这里仅用到MySQL，所以，这里我们仅安装MySQL依赖。

## data-diff CLI 工具

data-diff 提供了命令行工具。可以通过命令行工具完成数据库的连接和对比。

#### 1. data-diff CLI参数说明

- data-diff 帮助

查看帮助

```shell
data-diff --help

data-diff v0.9.13 - efficiently diff rows across database tables.

Usage:
  * In-db diff:    data-diff <database_a> <table_a> <table_b> [OPTIONS]
  * Cross-db diff: data-diff <database_a> <table_a> <database_b> <table_b> [OPTIONS]
  * Using config:  data-diff --conf PATH [--run NAME] [OPTIONS]

Options:
 ....

```

- 参数说明（部分）

![](./image/data-diff-help.png)

#### 2. data-diff CLI使用示例

我们的需求主要是对比两个MySQL数据库，这里以连接两个库为例。

- 对比表
```shell
data-diff mysql://root:abc123@localhost:3306/test_db user_table mysql://root:abc123@localhost:3307/test_db user_table

sockaddr ('127.0.0.1', 3306)
sockaddr ('127.0.0.1', 3307)
+ 22
+ 23
+ 24
```

默认以id为基准，对比第二个库新增的id。

- 对比表字段, 

`-c` 指定字段。

```shell
data-diff mysql://root:test#123@localhost:3306/test_db user_table mysql://root:test#123@localhost:3307/test_db user_table -c name -c email
```

- 对比主键
 
`-k` 指定对比主键

```shell
data-diff mysql://root:test#123@localhost:3306/test_db user_table mysql://root:test#123@localhost:3307/norma_db user_table -k email -c %_time
```

`-k` 指定唯一主键，不能为text类型。

- 设置最大不同数，

`-l` 设置limit。
```shell
data-diff mysql://root:test#123@localhost:3306/test_db sys_user mysql://root:test#123@localhost:3307/test_db sys_user -k email -l 10
```

对比工具最多找出 10 个不同就会停止。

#### 3. data-diff CLI 使用配置文件

命令行指定mysql数据库的链接配置太长了，也可以通过配置文件进行配置，然后指定配置文件即可。

- 编写配置文件

```conf
# datadiff.toml

## DATABASE CONNECTION ##
[database.new_db_connection] 
  driver = "mysql"
  database = "test_db"
  host = "127.0.0.1"
  port = "3306"
  user = "root"
  password = "pwd123"

[database.old_db_connection]
  driver = "mysql"
  database = "test_db"
  host = "127.0.0.1"
  port = "3307"
  user = "root"
  password = "pwd123"

## RUN PARAMETERS ##
[run.default]
  verbose = true

[run.confdiff]
  # Source 1 ("left")
  1.database = "new_db_connection"
  1.table = "user_table"

  # Source 2 ("right")
  2.database = "old_db_connection"
  2.table = "user_table"

  verbose = false
```

- 运行配置文件

```shell
data-diff --conf datadiff.toml --run confdiff -c email
```

## data-diff API使用

data-diff 项目的 tests 目录附带了大量的单元测试用例，基于单元测试用例，我们可以更深入的了解到data-diff 的API，我们可以直接调用这些API 来完成数据库表字段数据的对比。

- 测试数据库链接

```py
import unittest
from data_diff import connect


TEST_MYSQL_CONN_STRING: str = "mysql://mysql:Password1@localhost/mysql"


class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.mysql = connect(TEST_MYSQL_CONN_STRING)

    def test_connect_to_db(self):
        self.assertEqual(1, self.mysql.query("SELECT 1", int))


if __name__ == '__main__':
    unittest.main()
```

- 对比表数据（非完整代码）

```py
import unittest
from data_diff.hashdiff_tables import HashDiffer
from .common import *

@test_each_database
class TestDiffTables(DiffTestCase):
    src_schema = {"id": int, "userid": int, "movieid": int, "rating": float, "timestamp": datetime}
    dst_schema = {"id": int, "userid": int, "movieid": int, "rating": float, "timestamp": datetime}

    def setUp(self):
        super().setUp()
        self.table = table_segment(self.connection, self.table_src_path, "id", "timestamp", case_sensitive=False)
        self.table2 = table_segment(self.connection, self.table_dst_path, "id", "timestamp", case_sensitive=False)
        self.differ = HashDiffer(bisection_factor=3, bisection_threshold=4)
        
    def test_diff_small_tables(self):
        time = "2022-01-01 00:00:00"
        time_obj = datetime.fromisoformat(time)
        cols = "id userid movieid rating timestamp".split()
        self.connection.query(
            [
                self.src_table.insert_rows([[1, 1, 1, 9, time_obj], [2, 2, 2, 9, time_obj]], columns=cols),
                self.dst_table.insert_rows([[1, 1, 1, 9, time_obj]], columns=cols),
                commit,
            ]
        )
        diff_res = self.differ.diff_tables(self.table, self.table2)
        info = diff_res.info_tree.info
        diff = list(diff_res)
    
        expected = [("-", ("2", time + ".000000"))]
        self.assertEqual(expected, diff)
        self.assertEqual(2, info.rowcounts[1])
        self.assertEqual(1, info.rowcounts[2])
```

基于代码的灵活性，我们可以完成任何数据库的对比工作，比如，更复杂数据库多表聚合查询，将结果进行进行计算后比较等。
