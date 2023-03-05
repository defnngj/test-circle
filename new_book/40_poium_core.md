## poium 设计原理

poium 以简单易用得到广泛的使用，它的原理并不复杂，可以看作是一个语法糖，理论上可以支持任何 UI 测试库，包括 selenium、appium、playwright 等。

本小节我们就来实现 poium 的最小模型。


* 目录结构

```shell
├───poium_core
│   ├───__init__.py
│   └───page_object.py
└───test_poium_core.py
```

__功能代码__

实现 poium 核心代码。


```py
# poium_core/page_object.py


class Page:
    """
    定义Page类
    """
    def __init__(self, driver):
        self.driver = driver


class Element:
    """
    定义 Element 类
    """
    def __init__(self,  *locator):
        if len(locator) < 1:
            raise ValueError("Please specify only one locator")
        self.locator = locator

    def __get__(self, instance, owner):
        if instance is None:
            return None
        self.driver = instance.driver
        return self

    def input(self, text: str):
        """input 输入"""
        self.driver.find_element(*self.locator).send_keys(text)

    def click(self):
        """click 点击"""
        self.driver.find_element(*self.locator).click()

```

__代码说明:__

首先，实现 Page 类，__init\_\_() 初始化方法通过driver参数接收浏览器驱动。

接下来，实现 Element 类，__init\_\_()初始化方法通过 *locatior 参数接收元素定位。

__get\_\_() 是 python内置方法。如果类拥有这个方法的类，应该(也可以说是必须)产生一个实例，并且这个实例是另外一个类的类属性。其中，instance参数是通过该属性访问的实例，如果是通过所有者访问该属性，则为None。owner参数始终是Owner类。instance.driver 其实会拿到 Page 类的 self.driver 变量；这个跟 Page/Element类的用法有关。

input() 和 click() 方法是拿到驱动（self.driver）对元素的定位和操作。

> 扩展知识：
> 一个类只要实现了__get__，__set__，__delete__中任意一个方法，我们就可以叫它描述器(descriptor)。如果只定义了__get__我们叫非资料描述器(non-data descriptor)，如果__set__，__delete__任意一个/或者同时出现，我们叫资料描述器(data descriptor)。


__使用例子:__

通过例子演示 Page/Element 类的使用。

```py
# test_poium_core.py
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from poium_core.page_object import Page, Element


class BingPage(Page):
    """bing页面元素"""
    search_input = Element(By.ID, "sb_form_q")
    search_icon = Element(By.ID, "search_icon")


if __name__ == '__main__':
    driver = Chrome()
    driver.get("https://cn.bing.com")

    bp = BingPage(driver)
    bp.search_input.input("poium")
    bp.search_icon.click()

```

BingPage继承Page类，所以，通过 __init\_\_()方法需要指定浏览器驱动。Element类作为BingPage类的属性，所以，可以通过instance 拿到 BingPage 类的变量 self.driver。

这其实是一个很巧妙的设计，理解了这个知识点，poium就没有什么神秘的地方了。而且，我们可以举一反三将这个知识点应在任意地方。

