## 方法链（Method Chaining）

方法链接是Martin Fowler在他编写的《Domain Specific Languages》一书中提出的一种模式。在书中35页对方法链做了解释。

> Make modifier methods return the host object, so that multiple modifiers can be invoked in a single expression.

翻译成中文：修饰符方法返回宿主对象，以便在单个表达式中调用多个修饰符。

其实，实现起来并不复杂；我们在编写web自动化测试用例的时候，往往是：`打开` -> `输入` -> `输入` -> `点击` -> `输入` -> `点击` -> `检查` -> `关闭`.

这其实就是由一连串的动作组成。测试用例的步骤越长，编写的代码行数越多。以 Selenium 为例。

```py
from selenium import webdriver
from selenium.webdriver.common.by import By

dr = webdriver.Chrome()
dr.get("https://sample.com")
dr.find_element(By.ID, "xxx").send_keys("aaa")
dr.find_element(By.ID, "xxx").send_keys("bbb")
dr.find_element(By.ID, "xxx").click()
dr.find_element(By.ID, "xxx").send_keys("ccc")
dr.find_element(By.ID, "xxx").click()
dr.close()
```

当然，这样写代码并无什么不妥，但并不太符合人们去描述一件事情的过程。比如：

```
我今天早上去上班.
我去买了两个包子和一杯豆浆。
我去公交车站坐2路汽车。
我进公司大楼保安让我出示健康码。
我终于到了公司开始上班。
```

你会觉得这样描述很别扭，每句话都从`我`开始。如果改成：

```
我今天早上去上班，然后，先买了两个包子和一杯豆浆。一边吃一边去去公交车站坐2路汽车。终于到了公司楼下被保安拦下来我出示健康码。最后，终于到了公司开始上班。
```

好了，方法链其实更符合第二种方式去描述代码。而我们编写自动化用例其实就是几个常用方法之间反复调用，那么也更加适合用方法链来实现。


### 实现方法链的 API

基于方法链封装一套Selenium 的API。

```py
# webdriver_chinning.py
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


__all__ = ["Steps"]


class Selenium:
    driver = None   # 定义驱动
    element = None  # 定义元素
    alert = None    # 定义警告框


class Steps(object):
    """
    Webdriver Basic method chaining
    Write test cases quickly.
    """

    def __init__(self, url: str = None):
        Selenium.driver = Chrome()  # 默认浏览器
        self.url = url

    def open(self, url: str = None):
        """
        open url.

        Usage:
            open("https://www.baidu.com")
        """
        if self.url is not None:
            Selenium.driver.get(self.url)
        else:
            Selenium.driver.get(url)
        return self

    def find(self, css: str, index: int = 0):
        """
        find element
        """
        if len(css) > 5 and css[:5] == "text=":
            web_elem = Selenium.driver.find_elements(By.LINK_TEXT, css[5:])[index]
        elif len(css) > 6 and css[:6] == "text*=":
            web_elem = Selenium.driver.find_elements(By.PARTIAL_LINK_TEXT, css[6:])[index]
        else:
            web_elem = Selenium.driver.find_elements(By.CSS_SELECTOR, css)[index]
        Selenium.element = web_elem
        return self

    def type(self, text):
        """
        type text.
        """
        Selenium.element.send_keys(text)
        return self

    def click(self):
        """
        click.
        """
        Selenium.element.click()
        return self

    def close(self):
        """
        Closes the current window.

        Usage:
            close()
        """
        Selenium.driver.close()
        return self

    def alert(self):
        """
        get alert.
        Usage:
            alert()
        """
        Selenium.alert = Selenium.driver.switch_to.alert
        return self

    def accept(self):
        """
        Accept warning box.

        Usage:
            alert().accept()
        """
        Selenium.alert.accept()
        return self

    def dismiss(self):
        """
        Dismisses the alert available.

        Usage:
            alert().dismiss()
        """
        Selenium.driver.switch_to.alert.dismiss()
        return self

    def select(self, value: str = None, text: str = None, index: int = None):
        """
        Constructor. A check is made that the given element is, indeed, a SELECT tag. If it is not,
        then an UnexpectedTagNameException is thrown.
        """
        elem = Selenium.element
        if value is not None:
            Select(elem).select_by_value(value)
        elif text is not None:
            Select(elem).select_by_visible_text(text)
        elif index is not None:
            Select(elem).select_by_index(index)
        else:
            raise ValueError(
                '"value" or "text" or "index" options can not be all empty.')
        return self

    def sleep(self, sec: int):
        """
        Usage:
            sleep(seconds)
        """
        time.sleep(sec)
        return self
```

这里只封装了最常见的一些方法，你可以在此基础上扩展。

__定位元素__

```py
c = Steps()
c.find("#id")   # id
c.find(".class")  # class
c.find("[name=password]") # name 
c.find("div > tr > td")  # 多层级
c.find("div", 2)  # 定义一组元素，指定第几个
c.find("text=hao123")  # link text
c.find("text*=hao1")   # partial link text
```

* `find()`: 只支持CSS定位，这几乎是最强大的定位方法了。新的测试库`cypress`、`playwright`默认也都是CSS定位。

  * `text=` 用来定位文本。
  * `test*=` 用例模糊定位文本。

## 使用方法链

```py
# test_chinning.py
from webdriver_chinning import Steps

def test_case1():
    """百度搜索"""
    Steps(url="https://www.baidu.com").open().sleep(2).find("#kw").type("selenium").find("#su").click().close()
```

我们通过一行代码完成了一条用例的编写，这样的语法规则也更符合我们日常语言的描述。

但是，我们知道编辑器并不建议我们把一行代码写的过长，那么我们可以以适当的方式拆分。

```py
# test_chinning.py
from webdriver_chinning import Steps

def test_case2():
    """百度搜索"""
    s = Steps(url="https://www.baidu.com")
    s.open().sleep(2)
    s.find("#kw").type("selenium")
    s.find("#su").click()
    s.close()
```

当然，如果你更喜欢写到一行，那么也可以使用斜杠`\` 换行，来看一个稍微复杂一些例子。

```py
# test_chinning.py
from webdriver_chinning import Steps

def test_case3():
    """百度搜索设置"""
    Steps(url="http://www.baidu.com")\
            .open()\
            .find("#s-usersetting-top").click()\
            .find("#s-user-setting-menu > div > a.setpref").click().sleep(2)\
            .find('[data-tabid="advanced"]').click().sleep(2)\
            .find("#q5_1").click().sleep(2)\
            .find('[data-tabid="general"]').click().sleep(2)\
            .find("text=保存设置").click()\
            .alert().accept()\
            .close()
```

最后，方法链过长除了书写影响美观之外，最大的问题是当用例失败时定位问题非常麻烦，因为整个链条是一个整体，当用例失败时，很难确定是哪一节`链条`出了问题。正如文中给的例子一样，我们应该做适当的拆分。

用例已经过测试，可放心使用：

```shell
> pytest test_chinning.py
====================== test session starts ==========================
platform darwin -- Python 3.8.9, pytest-5.4.3, py-1.11.0, pluggy-0.13.1
rootdir: /Users/tech/klpro/github/test-circle/new_book/code/selenium_dev
plugins: metadata-1.11.0, html-2.1.1
collected 3 items

test_chinning.py ...                                             [100%]

====================== 3 passed in 30.57s ===========================
```

