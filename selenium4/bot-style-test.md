
# Bot Style Tests VS Page Objects

## Bot Style Tests

https://github.com/SeleniumHQ/selenium/wiki/Bot-Style-Tests

尽管 Page Objects 在你的测试中减少重复的方式是非常有用的，这并不总是一个团队愿意遵循的模式，另一种方法是遵循更`command-like`的测试风格。

一个`bot`是基于Selenium APIs 面向操作的抽象。这意味着如果你发现命令对你的应用程序没有做正确的事情，改变他们很容易。


```py
# bst.py
from selenium.webdriver.remote.webdriver import WebDriver


class ActionBot:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def submit(self, *locator):
        self.driver.find_element(*locator).submit()

    def type(self, *locator, text):
        elem = self.driver.find_element(*locator)
        elem.clear()
        elem.send_keys(text)
```

* 这其实相当于对Selenium API 的再次封装。

```py
# test_bst.py
from selenium.webdriver.common.by import By
from bst import ActionBot


def test_bst(browser):
    browser.get("http://www.baidu.com")

    action_bot = ActionBot(browser)
    action_bot.type(*(By.ID, "kw"), text="bot style tests")
    action_bot.click(*(By.ID, "kw"))
    time.sleep(5)
```

`*(By.ID, "kw")` - 这种写法不太常见，我单纯是为遵循文档上的写法。



## Page Objects

page objects 相信大家非常熟悉了，为了保持讨论的完整性，我还是给出例子。

```py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class Page:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    @property
    def search_input(self):
        return self.driver.find_element(By.ID, "kw")

    @property
    def search_button(self):
        return self.driver.find_element(By.ID, "su")
```

* 将每个元素封装为一个类方法。

```py
from po import Page

def test_po(browser):
    browser.get("http://www.baidu.com")
    page = Page(browser)
    page.search_input.send_keys("bot style tests")
    page.search_button.click()
```

* 对不同的元素对象进行操作。


## Bot Page

`Bot Page`是什么鬼？其实我们可以把上面的两种设计模式整合一下。在Page层既包含元素又包含动作。`Bot Page`是随便取的。

```py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class BotPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def type_search_input(self, text):
        self.driver.find_element(By.ID, "kw").send_keys(text)

    def click_search_button(self):
        self.driver.find_element(By.ID, "su").click()

```

* 元素定位和操作封装到一起。

```py
from po import BotPage

def test_bst_po(browser):
    browser.get("http://www.baidu.com")
    page = BotPage(browser)
    page.type_search_input("bot style tests")
    page.click_search_button()
```

* 这种方式就是最完美的吗？不是，这相当于强行将元素定位和操作绑定。但有时候一个元素可能有多种操作，比如输入框，`clear()`、`send_keys()`、`submit()` 都是可以的。

## 混用

三种模式并非相互对立，可以混合使用。比如，第一种和第三种混用。

```py
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class ActionBot:
    """bot style"""
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def submit(self, *locator):
        self.driver.find_element(*locator).submit()

    def type(self, *locator, text):
        elem = self.driver.find_element(*locator)
        elem.clear()
        elem.send_keys(text)


class BotPage(ActionBot):
    """ bot Page """
    def type_search_input(self, text):
        self.type(*(By.ID, "kw"), text=text)

    def click_search_button(self):
        self.click(By.ID, "su")
```

* 用 `bot Page` 去继承 `Action bot`，bot page 写起来就简单一些了。


## poium

当然，最简单的仍然是 poium。

https://github.com/SeldomQA/poium

```py
from poium import Page, Element, CSSElement

class PoiumPage(Page):
    search_input = Element(name='wd')
    search_button = Element(id_='su')

class CssPage(Page):
    search_input = CSSElement('#kw')
    search_button = CSSElement('#su')
```

* 他几乎是Page Objects设计模式的天花板了。程序员高质量Page objects测试库。

