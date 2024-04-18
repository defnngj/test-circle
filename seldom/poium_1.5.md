# 通用 Page Objects 库 poium


我曾在文章中多次介绍poium库，他是一个非常简单好用的 Page Objects 库。前几天，将 poium 更新到了`1.5.x` 版本，终于可以称之为`通用`的 Page Objects 库了。

### 说明与安装


__支持库：__

- [x] selenium ✔️
- [x] appium ✔️
- [x] playwright ✔️
- [x] uiautomator2 ⚠️
- [x] facebook-wda ️ ⚠️

如果你在使用Python做Web/App UI自动化测试，那么大概率会用到以上这些库。进一步，如果是你的自动化用例方便维护，那么大概率是需要用到Page Objects模式的。好了，poium的目标就是让你可以非常方便地使用Page Objects模式。

__特点：__


* 极简的Page层的元素定义。

> poium提供的是极简风格的Page Objects使用方式，他仅仅只是对元素的定位进行封装，不包含元素的操作，甚至是动作的整合。


* 支持主流的 Web/App UI库。

> 目前poium支持selenium、appium、playwright、uiautomator2、facebook-wda等， ⚠️ 表示还未充分测试。

* 对原生 API 无损。

> poium 不会对自动化库的API进行破坏，你可以在项目中随意的使用poium定义元素，或者只是某个元素用poium定义。


__安装：__

```shell
> pip install poium
> pip install playwright [可选]
> pip install uiautomator2 [可选]
> pip install facebook-wda [可选]
```

poium 集成了 `appium/selenium` 的依赖，为了保持 `poium` 足够轻量，其他库可选安装，因为我们一般也不会同时使用selenium 和 playwright，或者同时使用`appium` 和 `uiautomator2/facebook-wda`。


### 示例

给出简单的使用示例，更能帮你快速的上手 poium 的用法。

* selenium

```py
from selenium import webdriver
from poium import Page, Element, Elements


# page
class BaiduPage(Page):
    input = Element("#kw")
    button = Element("id=su")
    result = Elements("//div/h3/a", describe="搜索结果", timeout=2)


# selenium
driver = webdriver.Chrome()

page = BaiduPage(driver)
page.open("https://www.baidu.com")
page.input.send_keys("baidu")
page.button.click()

for r in page.result:
    print(r.text)

driver.close()
```

* appium

```py
from appium import webdriver
from appium.options.android import UiAutomator2Options
from poium import Page, Element


# page
class CalculatorPage(Page):
    number_1 = Element(id_="com.android.calculator2:id/digit_1")
    number_2 = Element(id_="com.android.calculator2:id/digit_2")
    add = Element(id_="com.android.calculator2:id/op_add")
    eq = Element(id_="com.android.calculator2:id/eq")


# appium
capabilities = {
    "automationName": "UiAutomator2",
    "platformName": "Android",
    'appPackage': 'com.android.calculator2',
    'appActivity': '.Calculator'
}
options = UiAutomator2Options().load_capabilities(capabilities)
driver = webdriver.Remote('http://localhost:4723/wd/hub', options=options)

page = CalculatorPage(driver)
page.number_1.click()
page.add.click()
page.number_2.click()
page.eq.click()

driver.quit()
```

* playwright 

```py
import re
from playwright.sync_api import sync_playwright
from playwright.sync_api import expect
from poium.playwright import Page, Locator


# page
class BingPage(Page):
    search_input = Locator('id=sb_form_q', describe="bing搜索框")
    search_icon = Locator('id=search_icon', describe="bing搜索按钮")


# playwright
with sync_playwright() as p:
    # 启动浏浏览器
    browser = p.chromium.launch(headless=False)
    # 创建新的页面
    page = browser.new_page()
    # 进入指定URL
    page.goto("https://cn.bing.com")

    # 获得元素
    search_page = BingPage(page)
    search_page.search_input.highlight()
    search_page.search_input.fill("playwright")
    search_page.search_icon.highlight()
    search_page.search_icon.screenshot(path="./docs/abc.png")
    search_page.search_icon.click()

    # 断言URL
    expect(page).to_have_title(re.compile("playwright"))

    # 关闭浏览器
    browser.close()
```

* uiautomator2 

```py
import uiautomator2 as u2

from poium.u2 import Page, XpathElement

# page
class BingPage(Page):
    search = XpathElement('//*[@resource-id="com.microsoft.bing:id/sa_hp_header_search_box"]')
    search_input = XpathElement('//*[@resource-id="com.microsoft.bing:id/sapphire_search_header_input"]')
    search_count = XpathElement('//*[@resource-id="count"]')


# uiautomator2
d = u2.connect()
d.app_start("com.microsoft.bing")
page = BingPage(d)
page.search.click()

page.search_input.click()
page.search_input.set_text("uiautomator2")
page.press("enter")

d.app_stop("com.microsoft.bing")
```

* facebook-wda

```py
import wda
from poium.wda import Page, Element


# page
class SomePage(Page):
    network = Element(label="蜂窝网络")
    battery = Element(label="电池")


# facebook-wda
c = wda.USBClient()
app = c.session("bundle_id")

sp = SomePage(c)
sp.network.get().click()
print("Element bounds:", sp.network.get().bounds)
app.screenshot()
app.swipe_right()
app.swipe_up()
sp.battery.scroll()
sp.battery.click()
```
