## 基于selenium API的二次开发

我们知道selenium的API非常简单，但其实并不算特别好用，比如数方法名比较长，例如`find_element_by_partial_link_text`，比如不能很好的支持元素显示等待。

有非常过的库或框架对其进行二次开发，甚至我们在编写Web UI自动化测试的时候也会对其进行二次封装，今天就教大家如何做二次封装，以及可以封装成哪些语法。

原生的selenium 代码如下：

```py
from selenium import webdriver
from selenium.webdriver.common.by import By


dr = webdriver.Chrome()
dr.get("https://www.baidu.com")

dr.find_element(By.ID, "kw").send_keys("selenium")
dr.find_element(By.ID, "su").click()

dr.quit()
```

## 封装1：方法重命名

这种封装，本质是只是把selenium API换了名字重写一遍，当然，好处就是更简洁了。

```py
# my_se.py
from selenium import webdriver
from selenium.webdriver.common.by import By


class MySe:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def open(self, url: str):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def by_id(self, elem: str):
        return self.driver.find_element(By.ID, elem)

    def by_name(self, elem: str):
        return self.driver.find_element(By.NAME, elem)

```

使用封装：

```py
from my_se import MySe

se = MySe()
se.open("https://www.baidu.com")
se.by_name("wd").send_keys("selenium")
se.by_id("su").click()
se.close()
```

把浏览器驱动给到`MySe()` 类就可以愉快的使用它的下面的方法了。


## 封装2：定位和动作整合

这种封装思路会将元素定位和操作动作整合成一个方法，至于 `定位类型`、`定位值` 或 `输入值` 作为方法参数。

```py
# you_se.py
from selenium import webdriver
from selenium.webdriver.common.by import By


class YouSe:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def open(self, url: str):
        self.driver.get(url)

    def close(self):
        self.driver.close()

    def get_element(self, **kwargs):
        by, value = next(iter(kwargs.items()))
        if by == "id":
            return self.driver.find_element(By.ID, value)
        if by == "name":
            return self.driver.find_element(By.NAME, value)
        else:
            pass

    def type(self, text: str, **kwargs):
        elem = self.get_element(**kwargs)
        elem.send_keys(text)

    def click(self, **kwargs):
        elem = self.get_element(**kwargs)
        elem.click()

```

使用封装：

```py
from you_se import YouSe

you = YouSe()
you.open("https://www.baidu.com")
you.type(name="wd", text="selenium")
you.click(id="su")
you.close()
```

注： `**kwargs ` 允许你将不定长度的键值对 作为参数传递给一个函数/方法。


## 封装3，独立每个方法

这种封装将每个操作都独立成一个函数，相互之间不产生关联。

```py
# her_se.py
from selenium import webdriver
from selenium.webdriver.common.by import By

dr = None


def start_chrome():
    global dr
    dr = webdriver.Chrome()


def go_to(url):
    global dr
    dr.get(url)


def close():
    global dr
    dr.close()


def id(elem):
    global dr
    return dr.find_element(By.ID, elem)

def name(elem):
    global dr
    return dr.find_element(By.NAME, elem)


def wirte(elem, text):
    elem.send_keys(text)


def click(elem):
    elem.click()

```

使用封装：

```py
from her_se import *


start_chrome()
go_to("http://www.baidu.com")
wirte(name("wd"), text="selenium")
click(id("su"))
close()
```

这个方法已经极简了，表面上看每个方法之间没有关联，但其实会依赖于`start_chrome()`函数的执行，这个函数用于创建驱动。


## 封装4，链式调用

链式调用就更加有意思了，我们可以像链条一样，把所有的方法串起来。

```py
# he_se.py
import time
from selenium import webdriver
from selenium.webdriver.common.by import By


class HeSe:

    def __init__(self):
        self.driver = webdriver.Chrome()

    def open(self, url: str):
        self.driver.get(url)
        return self

    def close(self):
        self.driver.close()
        return self

    def get_element(self, **kwargs):
        by, value = next(iter(kwargs.items()))
        if by == "id":
            return self.driver.find_element(By.ID, value)
        if by == "name":
            return self.driver.find_element(By.NAME, value)
        else:
            pass

    def type(self, text: str, **kwargs):
        elem = self.get_element(**kwargs)
        elem.send_keys(text)
        return self

    def click(self, **kwargs):
        elem = self.get_element(**kwargs)
        elem.click()
        return self
```


使用封装：

```py
from he_se import HeSe

he = HeSe()
he.open("https://www.baidu.com").type(name="wd", text="selenium").click(id="su").close()

```

链式调用可以一行代码把整个操作串联起来


## 最后

最后，文章中的例子实现的功能都是一样的：打开浏览器-> 到百度页面 -> 输入“selenium” -> 点击搜索 -> 关闭浏览器。

我们来做个简单统计：

1. 使用selenium API需要 232个字符。
2. 使用封装1（方法重命名）需要 141个字符。
3. 使用封装2（定位和动作整合）需要 135个字符。
4. 使用封装3（独立每个方法）需要 119个字符。
5. 使用封装4（链式调用）需要 121个字符。

相比原生的API，四种封装都比较明显的节省了代码量，然而，四种封装并没有特别明显的优略。当然，除了代码量还有`可读性` 也很重要。

selenium 作为一个非常成熟的Web UI自动化工具，已经被我们玩的很溜了，除了本文介绍的封装语法，应该还有更多的玩法。那么，你喜欢哪种写法呢？

