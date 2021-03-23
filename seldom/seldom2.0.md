# Seldom2.0: 如何更简单的实现HTTP接口测试

背景：

Seldom 1.0版本2020年1月发布到现在，更新20多个小版本，目前在做Web UI方面已经是一套比较成熟的方案了。之前，我创建过一个git分支，希望能把appium集成进来，因为appium和selenium本来就有很强的关联性。但是，目前来看国内使用openatx的用户更多，然而，openatx(uiautomator2/facebook-wda) 这样的库，由于API风格问题，比较难集成。后来，就暂时放弃了。

关于接口自动化框架，`土豆`同学曾创建了reudom，其实就是用seldom 整合了Requests库，API设计的不好，并没有什么两点，我本人也没有什么好的想法，就没有参与。其实，也不是完全没，只是没足够多的想法让我动手。

直到，前段时间有同学高速我cypress可以做接口测试，又让我有了想法为什么不把接口测试也集成到seldom里面。

* seldom本来就提供的有很好用的ddt，测试报告，这些接口自动化也需要啊。
* 在做UI自动化的时候，偶尔也需要调用接口去完成一些辅助工作。

如此看来，seldom支持HTTP接口测试两全齐美。

## 优势对比

先来看看unittest + requests 是如何来做接口自动化的：

```py
import unittest
import requests


class TestAPI(unittest.TestCase):

    def test_get_method(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        r = requests.get("http://httpbin.org/get", params=payload)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    unittest.main()
```

这其实，已经非常简洁，我甚至觉得这几行代码敲下来，比postman\JMeter之类的工具更加简单，效率更高。

同样的用例，用seldom实现。

```py
import seldom


class TestAPI(seldom.HttpRequest):

    def test_get_method(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        self.get("http://httpbin.org/get", params=payload)
        self.assertStatusCode(200)


if __name__ == '__main__':
    seldom.run()
```

主要简化点在，接口的返回数据的处理。当然，seldom真正的优势在日志和报告。打开debug模式`seldom.run(debug=True)` 运行上面的用例。

```shell
> python .\test_req_1.py
2021-03-24 00:54:30 [INFO] A run the test in debug mode without generating HTML report!
2021-03-24 00:54:30 [INFO]
            _      _
           | |    | |
 ___   ___ | |  __| |  ___   _ __ ___
/ __| / _ \| | / _` | / _ \ | '_ ` _ \
\__ \|  __/| || (_| || (_) || | | | | |
|___/ \___||_| \__,_| \___/ |_| |_| |_|
-----------------------------------------
                             @itest.info

test_get_method (test_req_1.TestAPI) ...
🚀 Request:--------------------------
method: GET
path: http://httpbin.org/get
🛬️ Response:------------------------
type: json
{'args': {'key1': 'value1', 'key2': 'value2'}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.25.0', 'X-Amzn-Trace-Id': 'Root=1-605a1d46-3cd15a151f0d46d20beda1d2'}, 'origin': '173.248.248.93', 'url': 'http://httpbin.org/get?key1=value1&key2=value2'}
ok

----------------------------------------------------------------------
Ran 1 test in 0.534s

OK
```

关闭debug模式，查看报告。

![](report.png)

通过日志/报告都可以清楚的看到。

* 请求的方法
* 请求url
* 响应的类型
* 响应的数据

## 更好强大的断言

断言接口返回的数据是我们在做接口自动化很重要的工作。



