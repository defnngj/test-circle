## 检查response装饰器

我们正在编写接口自动化测试的过程中，除了单接口测试，场景测试也非常重要。

例如测试支付业务的过程：

1. 用户登录
2. 加入购物
3. 下单
4. 支付

也就是说，如你想测试支付业务，大概必须要调用前面三个接口，那么就需要把前面三个接口进行封装。以用户登录为例。


```python
import json
import requests


class UserLogin:

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_token(self):
        """获取用户登录token"""
        url = "http://httpbin.org/post"

        data = {
            "username": self.username,
            "password": self.password,
            "token": "token123"  # 假装这是接口返回的toKen
        }
        r = requests.post(url, data=data)

        if r.status_code != 200:
            raise ValueError("接口请求失败")
        
        try:
            r.json()
        except json.decoder.JSONDecodeError:
            raise ValueError("接口不是json格式")

        if r.json()["headers"]["Host"] == "httpbin.org":
            raise ValueError("接口返回必要参数错误")
        
        token = r.json()["form"]["token"]
        return token


if __name__ == '__main__':
    login = UserLogin("zhangsan", "mima123")
    token = login.get_token()
    print(token)
```

单看接口这么封装，貌似没有问题！但每个接口调用之后都需要经历以下过程：

1. 判断状态码是否为 `200`，如果不是 `200` 说明接口不通。
2. 接着判断返回值格式是否为 `JSON`，如果不是可能接口返回数据格式错误，无法提取数据。
3. 检查接口返回的必要参数，例如：`r.json()["headers"]["Host"]`。
4. 提取接口返回的数据。例如: `r.json()["form"]["token"]`。


## 接口检查装饰器

基于以上的需求，可以实现 check_response() 装饰器来标准化处理这些问题。

```python
import json
from jmespath import search
from loguru import logger


def check_response(
        describe: str = "",
        status_code: int = 200,
        ret: str = None,
        check: dict = None,
        debug: bool = False):
    """
    检查返回的 response 数据
    :param describe: 接口描述
    :param status_code: 断言状态码
    :param ret: 提取返回的数据
    :param check: 检查接口返回的数据
    :param debug: 日志开关 Ture/False
    :return:
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            if debug is True:
                logger.info(f"Execute {func_name} - args: {args}")
                logger.info(f"Execute {func_name} - kwargs: {kwargs}")

            r = func(*args, **kwargs)
            flat = True
            if r.status_code != status_code:
                logger.info(f"Execute {func_name} - {describe} failed: {r.status_code}")
                flat = False

            try:
                r.json()
            except json.decoder.JSONDecodeError:
                logger.info(f"Execute {func_name} - {describe} failed：Not in JSON format")
                flat = False

            if debug is True:
                logger.info(f"Execute {func_name} - response:\n {r.json()}")

            if flat is True:
                logger.info(f"Execute {func_name} - {describe} success!")

            if check is not None:
                for expr, value in check.items():
                    data = search(expr, r.json())
                    if data != value:
                        logger.error(f"Execute {func_name} - check data failed：{value}")
                        raise ValueError(f"{data} != {value}")

            if ret is not None:
                data = search(ret, r.json())
                if data is None:
                    logger.warning(f"Execute {func_name} - return {ret} is None")
                return data
            else:
                return r.json()

        return wrapper

    return decorator
```
__代码说明：__

check_response() 装饰器 针对被装饰的 函数/方法 进行处理，所做的事情与前面一个例子相似。


__使用例子：__


```python
import requests
from common.extend import check_response


@check_response(
    describe="获取用户登录token",
    status_code=200,
    ret="form.token",
    check={"headers.Host": "httpbin.org"},
    debug=True)
def get_login_token(username, password):
    """获取用户登录token"""
    url = "http://httpbin.org/post"

    data = {
        "username": username,
        "password": password,
        "token": "token123"  # 预设是接口返回的toKen
    }
    r = requests.post(url, data=data)
    return r


if __name__ == '__main__':
    token = get_login_token("jack", "pawd123")
    print(token)

```

通过`@check_response()` 装饰接口调用函数，可以极大的减少样例代码的编写。参数说明：

* `获取用户登录token`: 接口描述。

* `200`: 检查接口返回值状态码是否为 `200`。

* `ret="form.token"`: 提取接口返回值中的`token`，利用`jmespath`提取器。

* `check={"headers.Host": "httpbin.org"}`: 检查接口返回值中包含的参数，相当于对接口数据进行断言。

* `debug=True`: 开启debug，打印详细信息，方便调试。


__运行结果__

```shell
> python user_login.py

2023-02-19 00:19:25.166 | INFO     | common.extend:wrapper:25 - Execute get_login_token - args: ('jack', 'pawd123')
2023-02-19 00:19:25.168 | INFO     | common.extend:wrapper:26 - Execute get_login_token - kwargs: {}
2023-02-19 00:19:27.005 | INFO     | common.extend:wrapper:41 - Execute get_login_token - response:
 {'args': {}, 'data': '', 'files': {}, 'form': {'password': 'pawd123', 'token': 'token123', 'username': 'jack'}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Content-Length': '45', 'Content-Type': 'application/x-www-form-urlencoded', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.28.1', 'X-Amzn-Trace-Id': 'Root=1-63f0fa8c-1d85b1c75be838872c3be4a0'}, 'json': None, 'origin': '113.118.187.221', 'url': 'http://httpbin.org/post'}
2023-02-19 00:19:27.008 | INFO     | common.extend:wrapper:44 - Execute get_login_token - 获取用户登录token success!
token123
```
