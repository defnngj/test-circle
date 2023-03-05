## 基于page object 的相关库

当我们真正理解 page object 的相关设计，采用那种写法都是可以的，除了纯手动编写 page 层的元素定位，有一些库来简化了 page 层的编写，我们也不妨拿来直接使用。


### selenium-page-factory


selenium-page-factory是一个Python库，他提供了page factory方法在 selenium 中实现page object模型。

特点：

* 一次初始化Point中声明的所有webElements。

* 所有的WebElements方法都被重新定义，以添加额外的功能，例如click方法扩展为显式等待元素可单击。

* 支持Selenium 4 ActionChains方法

* 现在支持Appium进行移动测试


* pip 安装

```shell
> pip install selenium-page-factory
```

__使用例子__

基于 selenium-page-factory 实现 Page 层的封装。

```py
# spf_page.py
from seleniumpagefactory.Pagefactory import PageFactory


class BingPage(PageFactory):

    def __init__(self, driver):
        self.driver = driver
        self.timeout = 15
        self.highlight = True

    # 使用PageFactory定义定位器字典
    locators = {
        "searchInput": ('ID', 'sb_form_q'),
        "searchIcon": ('ID', 'search_icon')
    }

    def search(self):
        # set_text(), click_button() 方法是PageFactory中的扩展方法
        self.searchInput.set_text("selenium-page-factory")
        self.searchIcon.click_button()

```

__代码说明__

创建BingPage类继承 PageFactory 类，重写父类的 __init\_\_() 初始化方法, 定义driver驱动，timeout 超时时间，以及 highlight 操作元素高亮。

licators 以字典的格式定义页面中操作的元素。

search() 方法用于封装业务动作，将搜索和点击封装成一个业务方法。

__使用例子__

调用 BingPage 层的封装。

```py
from selenium import webdriver
from spf_page import BingPage


driver = webdriver.Chrome()
driver.get("https://cn.bing.com")

bp = BingPage(driver)
bp.search()

```
调用 BingPage 传入驱动，然后调用 search() 方法即可完成搜索。


在使用 selenium-page-factory 的过程中发现两个问题。

1. 没有提供一组元素的返回或操作，例如搜索结果，需要拿到的是一个元素list，需要循环判断&打印text；或者通过index 索引获取第几个元素进行处理。这一点确实不方便。
2. Page 层的定义过重，即包含元素定位，又包含元素动作的整合，在测试脚本层面只剩下 调用 search() 方法了，这固然简化了操作，同时也失掉了灵活性。


## poium 

poium 是page object 模式的测试库，支持 appium/selenium/playwright等 UI测试库。

特点：

* 极大的简化了元素的定义。
* 对原生API无损。

pip 安装

```shell
> pip instal poium
```

__使用例子__

基于 poium 实现 Page 层的封装。

```py
# poium_page.py
from poium import Page, Element, Elements


class BingPage(Page):
    """bing 搜索页面"""
    search_input = Element(id_="sb_form_q", describe="bing搜索输入框", timeout=3)
    search_icon = Element(id_="search_icon", describe="bing搜索输入框", timeout=1)
    search_search = Elements(xpaht="//h2/a", describe="搜索结果", timeout=5)

```

__代码说明__

创建BingPage类继承 Page 类。

Element 和 Elements 用于定义单个元素和一组元素，describe 定义元素描述，timeout 指定超时时间。


__使用例子__

调用 BingPage 层的封装。

```py
from selenium import webdriver
from poium_page import BingPage


driver = webdriver.Chrome()
driver.get("https://cn.bing.com")

# 调用 BingPage 类
bp = BingPage(driver)
bp.search_input.send_keys("poium")
bp.search_icon.click()

# 打印搜索结果
result = bp.search_result
for r in result:
    print("搜索结果：", r.text)


```

调用 BingPage 传入驱动，然后，使用 BingPage 类中定义的元素完成 相应的操作。

__运行结果__

```
> python poium_demo.py

2023-03-05 18:39:35 logging.py | INFO | 🔍 Find element: id=sb_form_q. bing搜索输入框
2023-03-05 18:39:36 logging.py | INFO | ✅ send_keys('poium').
2023-03-05 18:39:36 logging.py | INFO | 🔍 Find element: id=search_icon. bing搜索输入框
2023-03-05 18:39:38 logging.py | INFO | ✅ click().
搜索结果： poium测试库介绍 - 虫师 - 博客园
搜索结果： SeldomQA/poium: Selenium/appium-based Page Objects …
搜索结果： poium · PyPI
搜索结果： python + Poium 库操作 - Test挖掘者 - 博客园
搜索结果： 【unittest单元测试框架】（10）poium 测试库 - hello_殷 - 博 …
搜索结果： poium测试库实现page_object模式_weixin_44160044的博客 ...
搜索结果： pytest自动化测试中的poium测试库_空城雀的博客-CSDN博客
搜索结果： GitHub - loveshanshan/poium
搜索结果： 当pytest遇上poium会擦出什么火花 - 虫师 - 博客园
搜索结果： python安装poi第三方库_python + Poium 库操作_段正淳你 ...
搜索结果： poium - 必应词典
搜索结果： Podium (2004) - IMDb
```

poium同样支持元素高亮显示，在运行的过程中更容易看清页面当前操作的元素。同时支持提供log日志，可以看到执行过程。

之所以说，poium 对原生API 无损，是因为他没有做“过度封装”，他只是把元素定义做了一层封装，你可以针对每个元素选择使用poium或者不使用，用法上非常灵活。
