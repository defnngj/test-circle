## 设计模式和开发策略

本章主要 探讨 Web/App UI 自动化测试中常用的设计模式 和 开发策略。


### page object

page object是一种在测试自动化中变得流行的设计模式，用于增强测试维护和减少代码重复。

__功能代码__

简单封装bing搜索相关元素定位，创建page_object.py

```py
# page_object.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BingPage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    @property
    def search_input(self):
        return self.driver.find_element(By.ID, "sb_form_q")

    @property
    def search_icon(self):
        return self.driver.find_element(By.ID, "search_icon")

```

__代码说明__

将Bing 的搜索输入框和icon的元素定位封装成方法，因为元素本身不需要传参，可以使用`@property`装饰器使方法只读属性。

__使用例子:__

调用 BingPage 类编写脚本。

```py
# test_page_object.py
from selenium.webdriver import Chrome
from page_object import BingPage

driver = Chrome()
driver.get("http://cn.bing.com")

# 调用BingPage类
page = BingPage(driver)
page.search_input.send_keys("bot style tests")
page.search_button.click()

```

自动化脚本层面，对不同的元素对象进行操作。


### bot Pattern


尽管 PageObjects 是减少测试重复的有用方法，但它并不总是团队愿意遵循的模式。另一种方法是遵循“command-like”风格的测试。


__功能代码__

封装元素的输入和点击，创建bot_style.py

```py
# bot_style.py
from selenium.webdriver.remote.webdriver import WebDriver


class ActionBot:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def click(self, *locator, times=1):
        """
        点击
        :param locator: 元素定位
        :param times: 点击次数
        :return:
        """
        elem = self.driver.find_element(*locator)
        for _ in range(times):
            elem.click()

    def type(self, *locator, text):
        """
        输入
        :param locator: 元素定位
        :param text: 输入文本
        :return:
        """
        elem = self.driver.find_element(*locator)
        elem.clear()
        elem.send_keys(text)

```

__代码说明__

这种设计更倾向于将元素的动作进行整合，例如 click() 方法可以增加 times 参数来控制点击次数；type() 方法可以增加 clear() 语句用于对输入框进行清空。 

__使用例子__

调用 ActionBot 类编写脚本。

```py
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from bot_style import ActionBot


driver = Chrome()
driver.get("https://cn.bing.com")

# 调用 ActionBot类
action_bot = ActionBot(driver)
action_bot.type(By.ID, "kw", text="bot style tests")
action_bot.click(By.ID, "su", times=1)

```

### 混合模式

我们实际在编写 page object 的可能太多细究 page object 和 bot style 两种模式的区别，甚至会混合使用两种设计。


__功能代码__

综合两种模式进行封装，创建hybrid_style.py

```py
# hybrid_style.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BingPage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def search_input(self, text="", enter=False):
        elem = self.driver.find_element(By.ID, "sb_form_q")
        elem.clear()
        elem.send_keys(text)
        if enter is True:
            elem.submit()

    def search_icon(self):
        self.driver.find_element(By.ID, "search_icon").click()

```

__代码说明__

你会看到我在 search\_input() 中除了元素定位，也放入了针对元素的动作， clear() 清空输入框、send_keys() 输入内容， subimit() 提交输入框等。search\_icon() 除了元素定位也放入 click() 点击动作。


__使用例子__


调用 BingPage 类编写脚本。

```py
from selenium.webdriver import Chrome
from hybrid_style import BingPage

driver = Chrome()
driver.get("http://cn.bing.com")

# 调用BingPage类
page = BingPage(driver)
page.search_input(text="bot style tests", enter=True)

```

由于 search_input() 的“过于封装”，可以通过 enter 参数来提交输入框的内容，自然也不用再 调用 search_icon() 方法来点击搜索icon了。这里所说的“过于封装” 并非贬义。


最后，不管纯正的 page object 、bot style 和 混合模式 之间并无优劣之分，他们只是一种编码风格，并不会对代码的最终执行结果产生影响，在工作可以结合项目看哪种写法更易于维护，以及更符合大家的习惯。
