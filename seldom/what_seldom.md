## seldom 自动化框架是什么？

seldom 是一个开源自动化测试框架。经过最近两年的频繁迭代，大大小小已经发布了几十个版本。我已经在多篇文章介绍他的特性和使用技巧。

但是，每次在介绍时评论区总会有网友提问，和xx相比有什么优势。受限与评论区的回复字数，我并不能很好的回答这个问题。那么，我觉得很有必要写一篇文章，介绍seldom是什么，有什么优势。

一句话概括：

> 基于unittest 的 Web UI/HTTP自动化测试框架。


### 基于 unittest 单元测试框架开发

为什么选择 `unittest` 单元测试框架？越来越多的人在使用 `pytest`, 他确实非常强大，并且有很丰富的生态（基于pytest的各种插件）。

我大概在2015年开始学习`pytest`，并分享了相关文章，并且也有在自动化项目中使用`pytest`，`pytest`确实非常强大，讲这个的原因是想说明，我并不顾不自封。

### 那为什么还选择基于`unittest`?

1. unittest是python自带的，这就意味着不需要额外安装。

2. 基于`unittest` 更容易实现封装，正因为他需要定义测试类，所以很容易在父类中实现API。你可能觉得pytest不需要写类更简单，但我在使用pytest的也会写类，类在我看来是一个很好的描述功能点的维度。一个文件表示一个`页面/业务`， 一个类表示一个`功能点`，一个方法表示一条`测试用例`，这其实是非常好的层次划分，所以，定义类对我来说不算负担。

下面是我用pytest写的代码：

```py
class TestLogin:

    @classmethod
    @pytest.fixture(scope="function", autouse=True)
    def setup(cls, driver):
        cls.page_menu = NavMenu(driver)
        cls.page_account = Account(driver)

    def test_normal_registered(self):
        """
        用例名称：输入未注册的邮箱，可注册成功
        """
        self.page_menu.switch_to_account()
        self.page_account.change_language_and_currency(language=Language.Simplified_Chinese)
        self.page_account.log_out()
        mail_mix = self.page_account.create_mix_string()
        user = "{email}@apptest.com".format(email=mail_mix)
        self.page_account.signup_password_check(email=user, password=AccountTest.password)
        assert self.page_account.account_credits.wait(self.page_menu.wait).exists()

    def test_check_short_password(self):
        """
        用例名称：输入密码123456，提示密码必须在8-20位包含字母和数字
        """
        self.page_menu.switch_to_account()
        self.page_account.log_out()
        mail_mix = self.page_account.create_mix_string()
        user = "{email}@apptest.com".format(email=mail_mix)
        self.page_account.signup_password_check(email=user, password="123456")
        assert self.page_account.snack_text.wait(self.page_account.wait).exists()
```

3. 我不喜欢 `pytest`的参数化。

```py
@pytest.mark.parametrize(
    "test_input, expected",
    [
        ("3+5", 8),
    ],
)
def test_eval(test_input, expected):
    assert eval(test_input) == expected
```

我承认`pytest` 的参数化非常强大，甚至可以使用多个`@pytest.mark.parametrize` 来实现笛卡尔积。但是，谁告诉我怎么才能不写 `"test_input, expected"`, 他谁让参数个数变的不灵活。

那么，我们看看 `unittest`+ `parameterized` 中的是如何实现参数化。 

```py
@parameterized([
    (2, 3, 5),
    (3, 5, 8),
])
def test_add(a, b, expected):
    assert_equal(a + b, expected)
```
看到了吗？ 他不需要定义个`"a, b, expected"` 在列表的上面。如果像`pytest` 那样，必须写成下面的样式。

```py
# unittest 模仿 pytest写法
@parameterized([
    "a, b, expected"
    (2, 3, 5),
    (3, 5, 8),
])
def test_add(a, b, expected):
    assert_equal(a + b, expected)
```
你可能觉得多写一行代码而已，这没什么？如果要参数化的是文件呢。

* data.json

```json
{
  "login":  [
    {
      "username": "Tom",
      "password": "tom123"
    },
    {
      "username": "Jerry",
      "password": "jerry123"
    }
  ]
}
```

* seldom

```py
@file_data("data.json", key="login")
def test_login(self, username, password):
    """a simple test case """
    print(username)
    print(password)
```

seldom 对 `parameterized` 做了二次开发，可以像上面那样使用。如果额外的再定义个`"username, password"` 不是很恶心吗？

好吧！我花了太多力气来说明`pytest`这个缺点了，但是，参数化真是的非常重要的特性，而且，`pytest` 的参数化写法是我不能接受的。


4. `seldom`补充了`unittest` 大部分缺点。
4.1 集成了定制的 HTML测试报告。

4.2 实现了用例依赖。

```py
import seldom
from seldom import depend


class TestDepend(seldom.TestCase):

    def test_001(self):
        print("test_001")

    @depend("test_001")
    def test_002(self):
        print("test_002")

    @depend("test_002")
    def test_003(self):
        print("test_003")
```

4.3 实现了分类标签

```py
import seldom
from seldom import label


class MyTest(seldom.TestCase):

    @label("base")
    def test_label_base(self):
        self.assertEqual(1+1, 2)

    @label("slow")
    def test_label_slow(self):
        self.assertEqual(1, 2)

    def test_no_label(self):
        self.assertEqual(2+3, 5)


if __name__ == '__main__':
    # seldom.main(debug=True, whitelist=["base"])  # whitelist
    seldom.main(debug=True, blacklist=["slow"])    # blacklist
```


### 相比 pytest 有什么优势

你认真看了上面的内容可能不会再问这个愚蠢的问题了，但如果没看也没关系，我在解答一遍。

* pytest 可以做web UI 自动化测试吗？

> 答案是否定的，必须要配合`selenium`, `playwright` 这样的web UI 测试库才行。

* pytest 可以做HTTP接口自动化测试吗？

> 答案是否定的，必须要配合`requests`, `httpx` 这样的HTTP库才行。

* seldom 可以做web UI 和 HTTP自动化测试吗？

> 答案是可定的，因为他已经集成了`selenium`，`requests`库。

