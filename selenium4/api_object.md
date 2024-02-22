## API Object Models


### API测试面临的问题

API测试由于编写简单，以及较高的稳定性，许多公司都以不同工具和框架维护API自动化测试。我们基于seldom框架也积累了几千条自动化用例。

* 简单的用例

```py
import seldom


class TestRequest(seldom.TestCase):

    def test_post_method(self):
        self.post('/post', data={'key':'value'})
        self.assertStatusCode(200)

    def test_get_method(self):
        payload = {'key1': 'value1', 'key2': 'value2'}
        self.get("/get", params=payload)
        self.assertStatusCode(200)

if __name__ == '__main__':
    seldom.main(base_url="http://httpbin.org")
```

* 场景测试用例

在复杂在场景中，比如，多个接口会用到的一些公共接口。

首先，封装一个公共类。

```py
# common.py
from seldom.request import check_response 
from seldom.request import HttpRequest


class Common(HttpRequest):
    
    @check_response(
        describe="获取登录用户名",
        status_code=200,
        ret="headers.Account",
        check={"headers.Host": "httpbin.org"},
        debug=True
    )
    def get_login_user(self):
        """
        调用接口获得用户名
        """
        headers = {"Account": "bugmaster"}
        r = self.get("http://httpbin.org/get", headers=headers)
        return r
```

然后，调用common编写用例。

```py
import seldom
from common import Common


class TestRequest(seldom.TestCase):

    def start(self):
        self.c = Common()

    def test_case(self):
        # 调用 get_login_user() 获取
        user = self.c.get_login_user()
        self.post("http://httpbin.org/post", data={'username': user})
        self.assertStatusCode(200)


if __name__ == '__main__':
    seldom.main(debug=True)
```

* 其他用例

还有一些用例是通过数据驱动文件（CSV\EXcel...等）维护的，这里就不举例了。


以上写法基本没有问题。但是，随着参与编写自动化的人变多，自动化用例不断增加。一些问题就暴露出来了。

> 比如，A测试需要多条用例需要用到登录，于是，将一个登录API封装成一个`user_login()`使用。B测试遇到这个场景大概率也会这么干！同样封装一个`user_login()`使用。庞大的自动化项目中会存在大量类似的冗余代码。当然录的API发生变化的时候，所有涉及到的用例或封装都需要修改。这个维护成本是很高的。
> 实际上，我们的项目就正在面临这个严重的问题。整个API自动化项目分多个团队，几十个人参与编写API测试用例&提交代码。没有引入清晰的分层设计，形成这些问题几乎是必然的。


### API Object Models

API Object Models，简称AOM，AOM是一种设计模式，它围绕着将API、路由或功能交互及其相关行为封装在结构良好的对象中。AOM旨在增强API测试和集成的直观性和弹性。在实践中，AOM需要精心设计专门的API对象，以有效地保护用户免受与API 请求、响应、端点交互和身份验证过程相关的复杂性的影响。


#### 基本概念


__AOM基本用法__

我们可以将业务高度关联的一组API封装为一个APIObject。例如，一个购物网站的API测试，我们可以创建一个`OrderAPIObject`来抽象化订单过程的复杂性。该对象封装了将商品添加到购物车、设置收件详细信息和下订单所需的API请求。测试脚本只需要与`OrderAPIObject`交互，从而简化了测试过程。

```py

class OrderAPIObject:

    def add_item_to_cart(self, item_id: str):
        """
        发出API请求和向购物车添加商品
        :param item_id:
        :return:
        """
        ...

    def set_shipping_details(self, details):
        """
        通过API请求设置收件信息
        :param details:
        :return:
        """
        ...

    def place_order(self):
        """
        下订单并接收确认
        :return:
        """
        ...
```

__创建API对象技巧__

为了创建强大的API对象，让我们进一步以`OrderAPIObject`为例。在此对象中，可以优雅地处理来自API的错误响应等场景。

```py

class OrderAPIObject:

    def __init__(self):
        # 调用前置方法
        self.prepare_order()

    def prepare_order(self):
        """
        准备下订单所需的项目和元素
        :return:
        """
        ...

    def place_order(self) -> dict:
        """
        下订单，以及处理错误响应
        :return: OrderConfirmation ErrorResponse
        """
        ...
```

可以在下单之前，调用`prepare_order()`方法执行一些下单的前置工作。`place_order()`方法可以包含处理异常的响应，以及返回错误结果，以便测试保持弹性。


__简单和灵活之间的平衡__

任何设计模式的一个关键考虑因素是在简单性和灵活性之间找到适当的平衡。

例如，一个处理用户注册的API。在AOM 中，可以选择将用户注册数据作为单独的参数传递，或者将它们封装在`User`对象（或接口）中。选择取决于测试的可读性和可维护性要求。

```py

class UserAPIObject:

    def register1(self, name: str, email: str, password: str):
        """
        实现用户注册API
        :param name:
        :param email:
        :param password:
        :return:
        """
        ...

    def register2(self, user: dict):
        """
        实现用户注册API
        :param user:
        :return:
        """
        name = user.get("name", "")
        email = user.get("email", "")
        password = user.get("password", "")
        ...
```

其中，`register1()`方法定义API所需要的每一个参数。当参数非常多时，也可以使用`register2()`方法直接接收dict对象。


#### AOM示例

通过模拟例子，演示基于AOM的接口自动化测试。

首先，定义APIObject层。

```py
# shop_object.py

class AuthAPIObject:

    def __init__(self, api_key):
        self.api_key = api_key

    def get_token(self, user_id:str) -> str:
        """
        模拟：根据用户ID生成登录token
        :param user_id:
        :return:
        """
        ...


class UserAPIObject:

    def __init__(self, token: str):
        self.token = token

    def get_user_data(self, user_id: str):
        """
        模拟：根据用户ID查询用户信息
        :param user_id:
        :return:
        """
        ...


class ProductAPIObject:

    def __init__(self, token: str):
        self.token = token

    def get_product_data(self, product_id: str):
        """
        模拟：根据产品ID查询产品信息
        :param product_id:
        :return:
        """
        ...
```

以上非完整代码，说明如下。

* AuthAPIObject类用于封装用户认证相关接口，`api_key`参数用于接收接口的关键key。`get_token()`方法返回用户登录token。

* UserAPIObject类用于封装用户相关接口，调用接口需要登录`token`。`get_user_data()`方法，通过user ID查询用户数据。

* UserAPIObject类用于封装商品相关接口，调用接口需要登录`token`。`get_product_data()`方法，通过product ID查询商品数据。

然后，在用例中调用APIObject层。

```py
import unittest
from shop_object import AuthAPIObject, UserAPIObject, ProductAPIObject

class APITest(unittest.TestCase):

    def setUp(self) -> None:
        auth_api = AuthAPIObject("api_key_123")
        self.token = auth_api.get_token("user123")

    def test_user_info(self):
        """
        用户信息查询接口
        """
        user_api = UserAPIObject(self.token)
        user_data = user_api.get_user_data("tom123")
        self.assertEqual(user_data["name"], "tom")

    def test_product_info(self):
        """
        商品信息查询接口
        """
        product_api = ProductAPIObject(self.token)
        product_data = product_api.get_product_data("product123")
        self.assertEqual(product_data["name"], u"潮流T恤")


if __name__ == '__main__':
    unittest.main()
```

### 总结

分层的好处立刻显现，

首先，API只允许通过的APIObject进行封装，那么在封装之前可以检索一下是否有封装了，如果有，进一步确认是否满足自己的调用需求，我们一般在测试API的时候一般各种参数验证，当API作为依赖接口调用的时候，一般参数比较少且固定，所以，API在封装的时候要兼顾到这两种情况。

其次，用例层只能通过APIObject的封装调用API，向登录token这种大部分接口会用到的信息，可以通过类初始化时传入，后续调用类下面方法的时候就不需要关心的。如果是多个接口组成一个场景，也可以再进行一层业务层的封装。

做好以上两点，就可以大大的减少代码冗余，后续维护起来也会方便很多。

你会发现 API Object 与 Page Object 思想基本一致，前者针对API测试，后者针对UI测试。关于API Object最早出处已经不可考了。以下为本文参考的文章：

https://medium.com/@khaled_arfaoui/api-object-model-a-functional-approach-to-test-your-apis-f982bad60f9f

