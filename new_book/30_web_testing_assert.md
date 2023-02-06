## 设计web测试断言

断言是自动化测试非常重要的一部分，一般断言由测试框架提供，通过断言来判断用例的通过或失败。单元测试框架仅提供了结果和类型断言：

unittest提供断言类型：


* assertEqual(a, b)： a == b

* assertNotEqual(a, b)：a != b

* assertTrue(x)：bool(x) is True

* assertFalse(x)：bool(x) is False

* assertIs(a, b): a is b

* assertIsNot(a, b): a is not b

* assertIsNone(x): x is None

* assertIsNotNone(x): x is not None

* assertIn(a, b): a in b

* assertNotIn(a, b): a not in b

* assertIsInstance(a, b): isinstance(a, b)

* assertNotIsInstance(a, b)

显然，这些类型，并不能直接适用 Web 自动化测试。web 自动化测试常用断言点。

* 页面标题
* 页面URL地址
* 页面文本信息
* 页面元素
* 新旧截图对比

以selenium 断言标题为例：

```py
import unittest
from selenium.webdriver import Chrome

class MyTest(unittest.TestCase):

    def test_case(self):
        driver = Chrome()
        driver.get("https://www.selenium.dev/")
        # 获取当前页面URL，进行断言
        current_title = driver.title
        self.assertEqual(current_title, "Selenium")

```

如果进行断言封装，可以将上面的两步，简化为一步实现。例如：

* 封装前

```py
current_title = driver.title
self.assertEqual(current_title, "Selenium")
```

* 封装后

```py
self.assertTitle("Selenium")
```

## 封装Selenium断言方法

基于前面的讲解，我们可以针对Selenium的API封装适用于Web自动化测试的断言方法。


__功能代码__

在Python中实现自定义异常类。

```py
# common/case.py

import unittest
from urllib.parse import unquote
from selenium.webdriver.common.by import By


# 定义浏览器驱动
class Browser:
    driver = None


# 定义unittest主方法
main = unittest.main


class TestCase(unittest.TestCase):
    """
    定义unittest测试类，实现断言方法
    """

    def assertTitle(self, title: str = None, msg: str = None) -> None:
        """
        断言当前页面标题是否等于title.

        用法:
            self.assertTitle("title")
        """
        if title is None:
            raise AssertionError("断言的title不能为空.")

        print(f"👀 assertTitle -> {title}.")
        self.assertEqual(title, Browser.driver.title, msg=msg)

    def assertInTitle(self, title: str = None, msg: str = None) -> None:
        """
        断言当前页面标题是否包含title.

        用法:
            self.assertTitle("title")
        """
        if title is None:
            raise AssertionError("断言的title不能为空.")

        print(f"👀 assertInTitle -> {title}.")
        self.assertIn(title, Browser.driver.title, msg=msg)

    def assertUrl(self, url: str = None, msg: str = None) -> None:
        """
        判断当前页面地址是否为url.

        用法:
            self.assertUrl("url")
        """
        if url is None:
            raise AssertionError("断言的url不能为空.")

        print(f"👀 assertUrl -> {url}.")
        current_url = unquote(Browser.driver.current_url)
        self.assertEqual(url, current_url, msg=msg)

    def assertInText(self, text: str = None, msg: str = None) -> None:
        """
        断言页面是否包含 text 文本.

        用法:
            self.assertInText("text")
        """
        if text is None:
            raise AssertionError("断言的text不能为空.")

        elem = Browser.driver.find_element(By.TAG_NAME, "html")
        print(f"👀 assertText -> {text}.")
        self.assertIn(text, elem.text, msg=msg)
```

__代码说明__

1. 定义 Browser 类，driver变量用于保存浏览器驱动，断言方法中涉及到Selenium的浏览器驱动方法，都基于Browser类的driver变量。

2. 将unittest.main 方法赋值给 main，目的是为了消除用例层对unittest的调用。

3. 创建TestCase类继承unittest的TestCase类，分别实现 assertTitle、assertInTitle、assertUrl， assertInText 等断言方法。


__使用例子__

基于上面的断言方法的封装，我们通过例子调用上面的断言。

```py
# test_assert.py
from selenium.webdriver import Chrome
from common.case import TestCase
from common.case import Browser
from common.case import main


class MyTest(TestCase):

    def setUp(self) -> None:
        Browser.driver = Chrome()

    def tearDown(self) -> None:
        Browser.driver.quit()

    def test_case(self):
        Browser.driver.get("https://www.selenium.dev/")
        self.assertTitle("Selenium")
        self.assertInTitle("Se")
        self.assertUrl("https://www.selenium.dev/")
        self.assertInText("Selenium automates browsers. That's it!")


if __name__ == '__main__':
    main()
```

__代码说明:__

创建MyTest类继承封装的TestCase类。

调用 selenium 的 Chrome类赋值给 Browser.driver, 基于 Browser.driver 完成接下来的页面操作。

在test_case用例中访问 selenium官网，分别调用父类中封装的断言方法。通过断言的方法，可以有效的简化了Web自动化测试中的断言。




