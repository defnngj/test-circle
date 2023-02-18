## 封装 HTTP 测试库 API 

本文以为requests 为例，介绍requests HTTP 测试库的封装。

requests 库的API已经足够简单了，没有太多可进一步封装空间。

```py
import requests

r = requests.get('https://api.github.com/events', params={'key': 'value'})
r = requests.post('https://httpbin.org/post', data={'key': 'value'})
r = requests.put('https://httpbin.org/put', data={'key': 'value'})
r = requests.delete('https://httpbin.org/delete', data={'key': 'value'})
```

## 集成日志系统

在做HTTP接口自动化的过程中，我们非常关心接口的请求信息，已经返回的结果。每次都 通过 print() 做打印其实也太方便，或者说不够效率。因此，我们可以集成日志，默认通过log输出这些信息。

* 目录结构

```
├───common
│   ├───__init__.py
│   ├───case.py
│   └───request.py
└───test_request.py
```

__功能代码__

实现request的封装。

```py
# common/request.py
import json
import requests
from loguru import logger


def formatting(msg):
    """格式化JSON数据"""
    if isinstance(msg, dict):
        return json.dumps(msg, indent=2, ensure_ascii=False)
    return msg


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

        status_code = r.status_code
        logger.info("-------------- 响应 ----------------")
        if status_code == 200 or status_code == 304:
            logger.info(f"successful with status {status_code}")
        else:
            logger.warning(f"unsuccessful with status {status_code}")
        resp_time = r.elapsed.total_seconds()
        try:
            resp = r.json()
            logger.debug(f"[type]: json      [time]: {resp_time}")
            logger.debug(f"[response]:\n {formatting(resp)}")
        except BaseException as msg:
            logger.debug("[warning]: failed to convert res to json, try to convert to text")
            logger.trace(f"[warning]: {msg}")
            r.encoding = 'utf-8'
            logger.debug(f"[type]: text      [time]: {resp_time}")
            logger.debug(f"[response]:\n {r.text}")

        return r

    return wrapper


class HttpRequest:
    """http request class"""

    @request
    def get(self, url, params=None, **kwargs):
        return requests.get(url, params=params, **kwargs)

    @request
    def post(self, url, data=None, json=None, **kwargs):
        return requests.post(url, data=data, json=json, **kwargs)

    @request
    def put(self, url, data=None, **kwargs):
        return requests.put(url, data=data, **kwargs)

    @request
    def delete(self, url, **kwargs):
        return requests.delete(url, **kwargs)
```


__代码说明__

1. 在 HttpRequests 类中重新实现 get、post、put、delete 四个方法，参数不变，分别调用requests提供的四个同名方法。使用@request 装饰器。

2. 实现 request 装饰器，获得请求和响应的相关数据，利用 logger 进行日志打印。打印 json 格式数据的部分调用 formatting 方法。

3. 实现 formatting方法，针对 json 格式的数据进行格式化。


集成到unittest框架中。

```py
# common/case.py
import unittest
from .request import HttpRequest

# 定义unittest主方法
main = unittest.main


class TestCase(unittest.TestCase, HttpRequest):
    """
    定义TestCase类，继承 unittest.TestCase 和 HttpRequest
    """
    pass

```

__代码说明__

这部分代码比较简单，将request封装的 HttpRequest与unittest 进行整合，统一对外提供API。


__使用例子__

基于上面的断言方法的封装，我们通过例子调用上面的断言。

```py
# test_request.py
from common.case import TestCase, main


class MyHttpTest(TestCase):

    def test_get(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = self.get('https://httpbin.org/get', params=payload)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    main()
```

__代码说明:__

创建测试类，继承 case 文件中的 TestCase 类； 在test_get() 测试方法中，直接通过 self.get() 使用 HttpRequest类中封装的方法，参数与用法与 requests 库保持一直。

__运行测试:__

```shell
> python test_request.py
2023-02-12 16:27:12.752 | INFO     | common.request:wrapper:18 - -------------- 请求 -----------------
2023-02-12 16:27:12.753 | INFO     | common.request:wrapper:24 - [method]: GET      [URL]: https://httpbin.org/get
2023-02-12 16:27:12.755 | DEBUG    | common.request:wrapper:38 - [params]:
 {
  "key1": "value1",
  "key2": "value2"
}
2023-02-12 16:27:14.046 | INFO     | common.request:wrapper:48 - -------------- 响应 ----------------
2023-02-12 16:27:14.048 | INFO     | common.request:wrapper:50 - successful with status 200
2023-02-12 16:27:14.049 | DEBUG    | common.request:wrapper:56 - [type]: json      [time]: 1.286827
2023-02-12 16:27:14.050 | DEBUG    | common.request:wrapper:57 - [response]:
 {
  "args": {
    "key1": "value1",
    "key2": "value2"
  },
  "headers": {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Host": "httpbin.org",
    "User-Agent": "python-requests/2.28.1",
    "X-Amzn-Trace-Id": "Root=1-63e8a2e3-772e3b303075f68b05e38c84"
  },
  "origin": "173.248.248.88",
  "url": "https://httpbin.org/get?key1=value1&key2=value2"
}
.
----------------------------------------------------------------------
Ran 1 test in 1.300s

OK
```

通过运行日志可以清晰的看到HTTP接口自动化的详细信息。
