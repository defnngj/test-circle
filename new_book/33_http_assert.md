## http 接口断言

对于HTTP接口来说，响应的数据主要以 JSON 格式为主。我需要针对JSON 格式的数据进行断言。

* JSON格式的数据

```json
{
  "code": 100200,
  "message": "success",
  "result": {
    "user_list": [
      {
        "id": 1,
        "name": "tom",
        "hobby": [
          "basketball",
          "swimming"
        ]
      },
      {
        "id": 2,
        "name": "jack",
        "hobby": [
          "skiing",
          "reading"
        ]
      }
    ]
  }
}
```

以上是一个比较典型的HTTP接口返回数据，我们为测试里面的数据，需要将json 转为 dict 格式进行提取。


```py
# 接口返回数据
resp = {  ...  }
# unittest 断言
self.assertEqual(resp["result"]["user_list"][0]["id"], 1)
self.assertEqual(resp["result"]["user_list"][0]["name"], "tom")
self.assertEqual(resp["result"]["user_list"][0]["hobby"][0], "basketball")
self.assertEqual(resp["result"]["user_list"][1]["name"], "jack")
self.assertEqual(resp["result"]["user_list"][1]["hobby"], ["skiing", "reading"])
```

JSON 数据结构越复杂，断言的提取语句越复杂。为此我可以封装一些断言方法简化，HTTP 接口的断言。


### assertPath 断言

JMESPath是一种JSON查询语言，用于从JSON文档中提取和转换元素。

jmespath文档: https://jmespath.org/specification.html

* pip 安装

```shell
> pip install jmespath
```

* jmespath 基本用法

```py
>>> import jmespath
>>> path = jmespath.search('foo.bar', {'foo': {'bar': 'baz'}})
'baz'
```

* 目录结构

```
├───common
│   ├───__init__.py
│   ├───config.py
│   ├───case.py
│   └───request.py
└───test_assert.py
```

注：请参考上一节目的项目代码，我们会在此基础上继续开发。

__功能代码__

增加配置文件 config.py

```py
# common/config.py

class ResponseResult:
    """配置：响应结果"""
    status_code = 200
    response = None

```

__代码说明：__

创建ResponseResult 类，用于保存测试结果。

---

修改 request.py 文件中的 request 装饰器

```py
# common/request.py
import json
import requests
from loguru import logger
from .config import ResponseResult


# ...
def request(func):
    """请求装饰器"""

    def wrapper(*args, **kwargs):
        func_name = func.__name__
        logger.info('-------------- 请求 -----------------')
        try:
            url = list(args)[1]
        except IndexError:
            url = kwargs.get("url", "")

        logger.info(f"[method]: {func_name.upper()}      [URL]: {url} ")
        auth = kwargs.get("auth", "")
        headers = kwargs.get("headers", "")
        cookies = kwargs.get("cookies", "")
        params = kwargs.get("params", "")
        data = kwargs.get("data", "")
        json_ = kwargs.get("json", "")
        if auth != "":
            logger.debug(f"[auth]:\n {auth}")
        if headers != "":
            logger.debug(f"[headers]:\n {formatting(headers)}")
        if cookies != "":
            logger.debug(f"[cookies]:\n {formatting(cookies)}")
        if params != "":
            logger.debug(f"[params]:\n {formatting(params)}")
        if data != "":
            logger.debug(f"[data]:\n {formatting(data)}")
        if json_ != "":
            logger.debug(f"[json]:\n {formatting(json_)}")

        # running function
        r = func(*args, **kwargs)

        # 响应状态码保存到 ResponseResult.status_code
        ResponseResult.status_code = r.status_code

        logger.info("-------------- 响应 ----------------")
        if ResponseResult.status_code == 200 or ResponseResult.status_code == 304:
            logger.info(f"successful with status {ResponseResult.status_code}")
        else:
            logger.warning(f"unsuccessful with status {ResponseResult.status_code}")
        resp_time = r.elapsed.total_seconds()
        try:
            resp = r.json()
            logger.debug(f"[type]: json      [time]: {resp_time}")
            logger.debug(f"[response]:\n {formatting(resp)}")
            
            # 响应结果保存到 ResponseResult.response
            ResponseResult.response = resp

        except BaseException as msg:
            logger.debug("[warning]: failed to convert res to json, try to convert to text")
            logger.trace(f"[warning]: {msg}")
            r.encoding = 'utf-8'
            logger.debug(f"[type]: text      [time]: {resp_time}")
            logger.debug(f"[response]:\n {r.text}")
            
            # 响应结果保存到 ResponseResult.response
            ResponseResult.response = r.text

        return r

    return wrapper

```

__代码说明：__

主要修改部分在 ResponseResult 类，用于保存 状态码 和 响应结果。


---

修改 case.py 类，增加 assertPath 断言方法。

```py
import unittest
import jmespath
from loguru import logger
from .request import HttpRequest
from .config import ResponseResult

# 定义unittest主方法
main = unittest.main


class TestCase(unittest.TestCase, HttpRequest):
    """
    定义TestCase类，继承 unittest.TestCase 和 HttpRequest
    """

    def assertPath(self, path, value):
        """
        断言 path 数据
        jmespath doc: https://jmespath.org/
        """
        logger.info(f"assertPath -> {path} >> {value}.")
        search_value = jmespath.search(path, ResponseResult.response)
        self.assertEqual(search_value, value)

```

__代码说明：__

jmespath.search() 方法根据 path 语法提取 ResponseResult.response 的响应数据，然后调用unittest 的  assertEqual() 断言是否等于预期值。

---

__使用例子__

基于上面的断言方法的封装，我们通过例子调用上面的断言。

```py
# test_assert.py
from common.case import TestCase, main


class MyHttpTest(TestCase):

    def test_assert(self):
        params = {
            "user_list": [
                {
                    "id": 1,
                    "name": "tom",
                    "hobby": ["basketball", "swimming"]
                },
                {
                    "id": 2,
                    "name": "jack",
                    "hobby": ["skiing", "reading"]
                }
            ]
        }
        self.post("https://httpbin.org/post", json=params)
        self.assertPath("json.user_list[0].id", 1)
        self.assertPath("json.user_list[0].name", "tom")
        self.assertPath("json.user_list[0].hobby[0]", "basketball")
        self.assertPath("json.user_list[1].name", "jack")
        self.assertPath("json.user_list[1].hobby", ["skiing", "reading"])


if __name__ == '__main__':
    main()
```

__代码说明:__

在test_assert() 测试方法中，使用父类中封装的 assertPath() 断言方法，第一个参数提取接口响应的数据，显然要比python中 dict 的提取更加简洁，第二个参数为要断言的值。

语法对比：

```py

self.assertEqual(resp["result"]["user_list"][0]["id"], 1)
self.assertPath("json.user_list[0].id", 1)

self.assertEqual(resp["result"]["user_list"][0]["name"], "tom")
self.assertPath("json.user_list[0].name", "tom")

self.assertEqual(resp["result"]["user_list"][0]["hobby"][0], "basketball")
self.assertPath("json.user_list[0].hobby[0]", "basketball")

self.assertEqual(resp["result"]["user_list"][1]["name"], "jack")
self.assertPath("json.user_list[1].name", "jack")

self.assertEqual(resp["result"]["user_list"][1]["hobby"], ["skiing", "reading"])
self.assertPath("json.user_list[1].hobby", ["skiing", "reading"])

```

__运行测试:__

```shell
> python test_assert.py

2023-02-12 23:14:21.468 | INFO     | common.request:wrapper:19 - -------------- 请求 -----------------
2023-02-12 23:14:21.469 | INFO     | common.request:wrapper:25 - [method]: POST      [URL]: https://httpbin.org/post
2023-02-12 23:14:21.471 | DEBUG    | common.request:wrapper:43 - [json]:
 {
  "user_list": [
    {
      "id": 1,
      "name": "tom",
      "hobby": [
        "basketball",
        "swimming"
      ]
    },
    {
      "id": 2,
      "name": "jack",
      "hobby": [
        "skiing",
        "reading"
      ]
    }
  ]
}
2023-02-12 23:14:22.700 | INFO     | common.request:wrapper:49 - -------------- 响应 ----------------
2023-02-12 23:14:22.702 | INFO     | common.request:wrapper:51 - successful with status 200
2023-02-12 23:14:22.704 | DEBUG    | common.request:wrapper:57 - [type]: json      [time]: 1.224992
2023-02-12 23:14:22.705 | DEBUG    | common.request:wrapper:58 - [response]:
 {
  "args": {},
  "data": "{\"user_list\": [{\"id\": 1, \"name\": \"tom\", \"hobby\": [\"basketball\", \"swimming\"]}, {\"id\": 2, \"name\": \"jack\", \"hobby\": [\"skiing\", \"reading\"]}]}",
  "files": {},
  "form": {},
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Content-Length": "137",
    "Content-Type": "application/json",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.28.1",
    "X-Amzn-Trace-Id": "Root=1-63e9024d-5d36511732339dd7682bf66c"
  },
  "json": {
    "user_list": [
      {
        "hobby": [
          "basketball",
          "swimming"
        ],
        "id": 1,
        "name": "tom"
      },
      {
        "hobby": [
          "skiing",
          "reading"
        ],
        "id": 2,
        "name": "jack"
      }
    ]
  },
  "origin": "173.248.248.88",
  "url": "https://httpbin.org/post"
}
2023-02-12 23:14:22.707 | INFO     | common.case:assertPath:21 - assertPath -> json.user_list[0].id >> 1.
2023-02-12 23:14:22.708 | INFO     | common.case:assertPath:21 - assertPath -> json.user_list[0].name >> tom.
2023-02-12 23:14:22.709 | INFO     | common.case:assertPath:21 - assertPath -> json.user_list[0].hobby[0] >> basketball.
2023-02-12 23:14:22.710 | INFO     | common.case:assertPath:21 - assertPath -> json.user_list[1].name >> jack.
2023-02-12 23:14:22.712 | INFO     | common.case:assertPath:21 - assertPath -> json.user_list[1].hobby >> ['skiing', 'reading'].
.
----------------------------------------------------------------------
Ran 1 test in 1.245s

OK
```

通过运行日志可以看到请求和响应数据，以及使用的断言方法。。


## assertJSON

如果要断言整个JSON 结构体，或者部分JSON结构体，assertPath()断言方法一个一个数据提取出来断言就显得过于麻烦了，我们设计assertJSON() 断言，通过传入整个结构体进行断言。

* 目录结构

```
├───common
│   ├───__init__.py
│   ├───utils.py
│   ├───config.py
│   ├───case.py
│   └───request.py
└───test_assert.py
```

注：请参考上一节目的项目代码，我们会在此基础上继续开发。


__功能代码__

在 utils.py 文件中实现 diff_json() 方法。

```py
# common/utils.py


class AssertInfo:
    """暂存断言信息"""
    warning = []
    error = []


def diff_json(response_data, assert_data):
    """
    递归：对比两个 JSON 数据格式
    """

    if isinstance(response_data, dict) and isinstance(assert_data, dict):
        # 字典格式
        for key in assert_data:
            if key not in response_data:
                AssertInfo.error.append(f"Error: Response data has no key: {key}")
        for key in response_data:
            if key in assert_data:
                # 递归
                diff_json(response_data[key], assert_data[key])
            else:
                AssertInfo.warning.append(f"Warning: Assert data has not key: {key}")

    elif isinstance(response_data, list) and isinstance(assert_data, list):
        # 列表格式
        if len(response_data) == 0:
            AssertInfo.warning.append("Warning: response is []")
        else:
            if isinstance(response_data[0], dict):
                try:
                    response_data = sorted(response_data, key=lambda x: x[list(response_data[0].keys())[0]])
                except TypeError:
                    response_data = response_data
            else:
                response_data = sorted(response_data)

        if len(response_data) != len(assert_data):
            AssertInfo.warning.append(f"Warning: List length is not equal: '{len(response_data)}' != '{len(assert_data)}'")

        if len(assert_data) > 0:
            if isinstance(assert_data[0], dict):
                try:
                    assert_data = sorted(assert_data, key=lambda x: x[list(assert_data[0].keys())[0]])
                except TypeError:
                    assert_data = assert_data
            else:
                assert_data = sorted(assert_data)

        for src_list, dst_list in zip(response_data, assert_data):
            # 递归
            diff_json(src_list, dst_list)
    else:
        if str(response_data) != str(assert_data):
            AssertInfo.error.append(f"Error: Value are not equal: {response_data}")

```

__代码说明:__

创建AssertInfo类，warning 变量用例收集 警告信息，error 变量用于收集错误信息。对于两种类型信息的定义：

* warning: 返回数据（`response_data`）中有，断言数据（`assert_data`）中没有，既然断言数据中没有定义，说明该数据不重要，以警告的方法收集。

* error: 返回数据（`response_data`）中没有，断言数据（`assert_data`）中有，既然断言数据明确定义，说明该数据非常重要，以为错误的方式收集。

diff_json() 是一个递归方法，用于接收 “返回数据（`response_data`）” 和 “断言数据（`assert_data`）” 两个参数，需要对参数的类型进行判断，根据参数类型 进行对比，如果是 list 类型通过 zip 打包为元组，然后循环调用 `diff_json()` 继续递归；如果是 dict 类型就通过 sorted() 进行排序；然后逐一进行比对。 

在对比的过程中 通过 AssertInfo 的 warning 和 error 变量分别记录告警和错误信息。

---

在 case.py 文件中新增 assertJSON 断言方法。

```py
import unittest
from loguru import logger
from .request import HttpRequest
from .config import ResponseResult
from .utils import AssertInfo, diff_json

# 定义unittest主方法
main = unittest.main


class TestCase(unittest.TestCase, HttpRequest):
    """
    定义TestCase类，继承 unittest.TestCase 和 HttpRequest
    """

    def assertJSON(self, assert_json, response=None):
        """
        断言 JSON 数据
        :param assert_json: 断言的JSON数据
        :param response: 断言的response，默认为None
        """
        logger.info(f"assertJSON -> {assert_json}.")
        if response is None:
            response = ResponseResult.response

        AssertInfo.warning = []
        AssertInfo.error = []
        diff_json(response, assert_json)
        if len(AssertInfo.warning) != 0:
            logger.warning(AssertInfo.warning)
        if len(AssertInfo.error) != 0:
            self.assertEqual("Response data", "Assert data", msg=AssertInfo.error)

```

__代码说明__

在 assertJSON() 断言方法中，assert_json 用于接收要断言的JSON数据，response默认为None, 通过 ResponseResult.response 获取接口响应的整个数据。

需要将 AssertInfo 下面的 warning 和 error 变量的值置空，以免影响下个数据的断言。

调用diff_json() 递归方法进行断言。

判断 AssertInfo.warning 的 list 不为空，就通过 logger 打印 AssertInfo.warning 收集的告警信息；判断  AssertInfo.error 的 list 不为空，就设置用例失败，并打印 AssertInfo.error 收集的错误信息。

---


__使用例子__

基于上面的断言方法的封装，我们通过例子调用上面的断言。

```py
# test_assert.py
from common.case import TestCase, main


class MyHttpTest(TestCase):

    def test_assert_json(self):
        # 接口参数
        payload = {"name": "tom", "hobby": ["basketball", "swim"]}
        # 接口调用
        resp = self.get("http://httpbin.org/get", params=payload)

        # 1.从整个response中断言。
        assert_data1 = {
            "args": {
                "hobby": ["swim", "basketball"],
                "name": "tom"
            }
        }
        self.assertJSON(assert_data1)

        # 2. 从部分 response 中断言。
        assert_data2 = {
            "hobby": ["swim", "basketball"],
            "name": "tom"
        }
        self.assertJSON(assert_data2, resp.json()["args"])


if __name__ == '__main__':
    main()
```

__代码说明:__

assertJSON() 断言方法的用法分两种。

1. 从整个response中断言，不需要第二个参数，要求assert_data 写出完整的路径。

2. 从部分response中断言，需要填第二个参数，指定response 要断言的是那部分数据。

__运行测试:__

```shell
> python test_assert.py

2023-02-18 22:21:12.084 | INFO     | common.request:wrapper:19 - -------------- 请求 -----------------
2023-02-18 22:21:12.086 | INFO     | common.request:wrapper:25 - [method]: GET      [URL]: http://httpbin.org/get
2023-02-18 22:21:12.087 | DEBUG    | common.request:wrapper:39 - [params]:
 {
  "name": "tom",
  "hobby": [
    "basketball",
    "swim"
  ]
}
2023-02-18 22:21:15.749 | INFO     | common.request:wrapper:51 - -------------- 响应 ----------------
2023-02-18 22:21:15.752 | INFO     | common.request:wrapper:53 - successful with status 200
2023-02-18 22:21:15.753 | DEBUG    | common.request:wrapper:59 - [type]: json      [time]: 1.563222
2023-02-18 22:21:15.755 | DEBUG    | common.request:wrapper:60 - [response]:
 {
  "args": {
    "hobby": [
      "basketball",
      "swim"
    ],
    "name": "tom"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.28.1",
    "X-Amzn-Trace-Id": "Root=1-63f0ded9-26e82a525de9391b6c4be023"
  },
  "origin": "113.118.187.221",
  "url": "http://httpbin.org/get?name=tom&hobby=basketball&hobby=swim"
}
2023-02-18 22:21:15.756 | INFO     | common.case:assertJSON:34 - assertJSON -> {'args': {'hobby': ['swim', 'basketball'], 'name': 'tom'}}.
2023-02-18 22:21:15.758 | WARNING  | common.case:assertJSON:42 - ['Warning: Assert data has not key: headers', 'Warning: Assert data has not key: origin', 'Warning: Assert data has not key: url']
2023-02-18 22:21:15.759 | INFO     | common.case:assertJSON:34 - assertJSON -> {'hobby': ['swim', 'basketball'], 'name': 'tom'}.
.
----------------------------------------------------------------------
Ran 1 test in 3.676s

OK
```

运行日志可以更好的帮助你理解两种用法的区分。 第一种用法属于包含判断，会以警告的方式打印 response 中没有断言的数据。第二种方法属于相等判断，所以不会有告警，如果两者不相等，则断言失败。


## assertJSON

有时候，我们不关心数据本身是什么，而是需要断言数据的结构体，以及数据的类型。例如：

```json
{
    "result": {
        "id": 1, 
        "token": "ahodfjasdfh1234h324kh2l3k",
        "data_time": "2022-11-12 12:00:00"
    }
}
```

在上面的JSON 数据中，只关心 result 中有 id，且为 int 类型即可，至于id 的值是 1 还 999 不重要；以此类推，token 和 data_time 的值只要是 string类型即可。

JSONSchema 是一种声明性语言，可用于注释和验证 JSON 文档。它刚好可以用来解决上述问题。

JSONSchema官网: https://json-schema.org/

* pip 安装

```shell
> pip install jsonschema
```

* jmespath 基本用法

```py
>>> from jsonschema import validate

>>> # A sample schema, like what we'd get from json.load()
>>> schema = {
...     "type" : "object",
...     "properties" : {
...         "price" : {"type" : "number"},
...         "name" : {"type" : "string"},
...     },
... }

>>> # If no exception is raised by validate(), the instance is valid.
>>> validate(instance={"name" : "Eggs", "price" : 34.99}, schema=schema)
```

* 目录结构

```
├───common
│   ├───__init__.py
│   ├───utils.py
│   ├───config.py
│   ├───case.py
│   └───request.py
└───test_assert.py
```

注：请参考上一节目的项目代码，我们会在此基础上继续开发。


__功能代码__

在 case.py 文件中实现 assertSchema() 断言方法。

```py
# common/case.py
import unittest
from loguru import logger
from jsonschema import validate
from jsonschema.exceptions import ValidationError
from .request import HttpRequest
from .config import ResponseResult


# 定义unittest主方法
main = unittest.main


class TestCase(unittest.TestCase, HttpRequest):
    """
    定义TestCase类，继承 unittest.TestCase 和 HttpRequest
    """

    def assertSchema(self, schema, response=None):
        """
        Assert JSON Schema
        doc: https://json-schema.org/
        :param schema: 断言的 schema 数据
        :param response: 断言的response，默认为None
        """
        logger.info(f"assertSchema -> {schema}.")

        if response is None:
            response = ResponseResult.response

        try:
            validate(instance=response, schema=schema)
        except ValidationError as msg:
            self.assertEqual("Response data", "Schema data", msg)

```

__代码说明:__

定义assertSchema 断言方法，第一个参数用于接收schema 格式的数据；第二个参数为response，默认为None, 即断言整个接口响应数据。

调用 提供的validate方法进行判断，ValidationError 用于捕捉异常，如果出现异常则以断言失败的方式抛出msg错误。


__使用例子__

基于上面的断言方法的封装，我们通过例子调用上面的断言。

```py
# test_assert.py
from common.case import TestCase, main


class MyHttpTest(TestCase):

    def test_assert_schema(self):
        # 接口参数
        payload = {"hobby": ["basketball", "swim"], "name": "tom"}
        # 调用接口
        resp = self.get("http://httpbin.org/get", params=payload)

        # 1.从整个response中断言
        assert_data1 = {
            "type": "object",
            "properties": {
                "args": {
                    "type": "object",
                    "properties": {
                        "hobby": {
                            "type": "array", "items": {"type": "string"}
                        },
                        "name": {
                            "type": "string"
                        }
                    }
                }
            }
        }
        self.assertSchema(assert_data1)

        # 从部分 response 中断言
        assert_data2 = {
            "type": "object",
            "properties": {
                "hobby": {
                    "type": "array", "items": {"type": "string"}
                },
                "name": {
                    "type": "string"
                }
            }
        }
        self.assertSchema(assert_data2, resp.json()["args"])


if __name__ == '__main__':
    main()
```

__代码说明:__

assert_data 定义断言的数据结构和类型，type 指定类型，dict 为 object, list 为 array，然后就是具体数据的类型 string 、integer、boolean 等，这里的类型定义与python 有所区别。如果数据是object对象，需要使用 properties 定义下一级数据。

assertSchema() 断言方法的用法同样分两种。

1. 从整个response中断言，不需要第二个参数，要求 assert_data 写出完整的结构。

2. 从部分response中断言，需要填第二个参数，指定response 要断言的是那部分数据。


__运行测试:__

```shell
> python test_assert.py

2023-02-18 23:53:35.631 | INFO     | common.request:wrapper:19 - -------------- 请求 -----------------
2023-02-18 23:53:35.633 | INFO     | common.request:wrapper:25 - [method]: GET      [URL]: http://httpbin.org/get
2023-02-18 23:53:35.634 | DEBUG    | common.request:wrapper:39 - [params]:
 {
  "hobby": [
    "basketball",
    "swim"
  ],
  "name": "tom"
}
2023-02-18 23:53:36.203 | INFO     | common.request:wrapper:51 - -------------- 响应 ----------------
2023-02-18 23:53:36.206 | INFO     | common.request:wrapper:53 - successful with status 200
2023-02-18 23:53:36.207 | DEBUG    | common.request:wrapper:59 - [type]: json      [time]: 0.565353
2023-02-18 23:53:36.209 | DEBUG    | common.request:wrapper:60 - [response]:
 {
  "args": {
    "hobby": [
      "basketball",
      "swim"
    ],
    "name": "tom"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.28.1",
    "X-Amzn-Trace-Id": "Root=1-63f0f47f-3f45cb9743445b8947bedaae"
  },
  "origin": "113.118.187.221",
  "url": "http://httpbin.org/get?hobby=basketball&hobby=swim&name=tom"
}
2023-02-18 23:53:36.211 | INFO     | common.case:assertSchema:55 - assertSchema -> {'type': 'object', 'properties': {'args': {'type': 'object', 'properties': {'hobby': {'type': 'array', 'items': {'type': 'string'}}, 'name': {'type': 'string'}}}}}.
2023-02-18 23:53:36.213 | INFO     | common.case:assertSchema:55 - assertSchema -> {'type': 'object', 'properties': {'hobby': {'type': 'array', 'items': {'type': 'string'}}, 'name': {'type': 'string'}}}.
.
----------------------------------------------------------------------
Ran 1 test in 0.584s

OK
```

