# 数据驱动设计

数据驱动是自动化测试框架非常重要的特性，尤其是在做接口自动化测试时，通过数据文件管理测试数据可以极大的节省用例编写的代码量。

## unittest数据驱动扩展

在unittest单元测试框架中提供了两个扩展

* parameterized: https://github.com/wolever/parameterized

* ddt: https://github.com/datadriventests/ddt


__Parameterized用法__

Parameterized是Python的一个参数化库，同时支持unittest、Nose和pytest单元测试框架（注：最新版的pytest已经不再支持）。

```shell
> pip install parameterized
```

通过Parameterized实现参数化。

```py
# parameterized_demo.py
import unittest
from parameterized import parameterized


class AddTestCase(unittest.TestCase):

    @parameterized.expand([
        ("2 and 3", 2, 3, 5),
        ("10 and 20", 10, 20, 30),
        ("hello and word", "hello", "world", "helloworld"),
    ])
    def test_add(self, _, a, b, expected):
        self.assertEqual(a + b, expected)


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

__代码说明：__

首先，导入Parameterized库下面的`parameterized`类。

其次，通过`@parameterized.expand()`来装饰测试用例`test_add()`。

在`@parameterized.expand()`中，每个元组被认为是一条测试用例。`Parameterized`默认把元组的第一个参数解析为用例名称的结尾部分。

最后，使用unittest的main()方法，设置verbosity参数为2，输出更详细的执行日志。

__运行结果：__

```shell
test_add_0_2_and_3 (__main__.AddTestCase) ... ok
test_add_1_10_and_20 (__main__.AddTestCase) ... ok
test_add_2_hello_and_word (__main__.AddTestCase) ... ok

----------------------------------------------------------------------
Ran 3 tests in 19.068s

OK
```

### ddt 用法

DDT（Data-Driven Tests）是针对unittest单元测试框架设计的扩展库。允许使用不同的测试数据来运行一个测试用例，并将其展示为多个测试用例。

* pip安装。

```shell
> pip install ddt
> pip install pyyaml
```
注：ddt 支持 YAML格式的数据驱动文件，需要安装pyyaml库。

通过ddt实现参数化。

```py
# ddt_demo.py
import unittest
from ddt import ddt, data, unpack


@ddt
class TestDTT(unittest.TestCase):

    @data([1, 2, 3], [4, 5, 9], [6, 7, 13])
    @unpack
    def test_add_list(self, a, b, c):
        self.assertEqual(a+b, c)

    @data(("Hi", "HI"), ("hello", "HELLO"), ("world", "WORLD"))
    @unpack
    def test_upper_tuple(self, s1, s2):
        self.assertEqual(s1.upper(), s2)

    @data({"d": "hello world", "t": str},
          {"d": 110, "t": int},
          {"d": True, "t": bool})
    @unpack
    def test_data_type_dict(self, d, t):
        self.assertTrue(isinstance(d, t))


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

__代码说明：__

首先，测试类需要通过`@ddt`装饰器进行装饰。

其次，DDT提供了不同形式的参数化。这里列举了三组参数化，第一组为列表，第二组为元组，第三组为字典。

最后，需要注意，字典的key与测试方法的参数要保持同名。

__运行结果：__

```shell
test_add_list_1__1__2__3_ (__main__.TestBaidu) ... ok
test_add_list_2__4__5__9_ (__main__.TestBaidu) ... ok
test_add_list_3__6__7__13_ (__main__.TestBaidu) ... ok
test_data_type_dict_1 (__main__.TestBaidu) ... ok
test_data_type_dict_2 (__main__.TestBaidu) ... ok
test_data_type_dict_3 (__main__.TestBaidu) ... ok
test_upper_tuple_1___Hi____HI__ (__main__.TestBaidu) ... ok
test_upper_tuple_2___hello____HELLO__ (__main__.TestBaidu) ... ok
test_upper_tuple_3___world____WORLD__ (__main__.TestBaidu) ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.002s

OK
```

利用JSON/YAML文件实现参数化。

* 目录结构

```tree
├───data  // 数据驱动文件目录
│   ├───test_data.json
│   └───test_data.yaml
├───ddt_demo2.py
```

* JSON数据文件

```json
# data/test_data.json
{
    "positive_integer_range": {
        "start": 0,
        "end": 2,
        "value": 1
    },
    "negative_integer_range": {
        "start": -2,
        "end": 0,
        "value": -1
    },
    "positive_real_range": {
        "start": 0.0,
        "end": 1.0,
        "value": 0.5
    }
}
```

* YAML数据文件

```yaml
positive_integer_range:
    start: 0
    end: 2
    value: 1

negative_integer_range:
    start: -2
    end: 0
    value: -1

positive_real_range:
    start: 0.0
    end: 1.0
    value: 0.5
```

* 测试用例

```py
# ddt_demo2.py
import unittest
from ddt import ddt, file_data


@ddt
class TestDDT(unittest.TestCase):

    @file_data('data/test_data.json')
    def test_file_data_json(self, start, end, value):
        self.assertLess(start, end)
        self.assertLess(value, end)
        self.assertGreater(value, start)

    @file_data('data/test_data.yaml')
    def test_file_data_yaml(self, start, end, value):
        self.assertLess(start, end)
        self.assertLess(value, end)
        self.assertGreater(value, start)


if __name__ == '__main__':
    unittest.main(verbosity=2)
```

__代码说明：__

首先，将测试数据写入到JSON/YAML文件中，然后，通过`@file_data` 装饰器指定测试文件的路径。

再此说明，如果想运行YAML的数据文件，需安装`pyyaml`库。

__运行结果：__

```shell
test_file_data_json_1_positive_integer_range (__main__.TestDDT)
test_file_data_json_1_positive_integer_range ... ok
test_file_data_json_2_negative_integer_range (__main__.TestDDT)
test_file_data_json_2_negative_integer_range ... ok
test_file_data_json_3_positive_real_range (__main__.TestDDT)
test_file_data_json_3_positive_real_range ... ok
test_file_data_yaml_1_positive_integer_range (__main__.TestDDT)
test_file_data_yaml_1_positive_integer_range ... ok
test_file_data_yaml_2_negative_integer_range (__main__.TestDDT)
test_file_data_yaml_2_negative_integer_range ... ok
test_file_data_yaml_3_positive_real_range (__main__.TestDDT)
test_file_data_yaml_3_positive_real_range ... ok

----------------------------------------------------------------------
Ran 6 tests in 0.002s

OK
```

