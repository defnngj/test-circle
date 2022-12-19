# Seldom3.0: 支持App测试

官方文档：https://seldomqa.github.io/

## seldom 版本回顾

2015年7月15号我在github上提交一个项目，取名为：pyse = python + selenium。 项目非常简单核心就三个。

* `pyse.py`： 针对 selenium API做了简单封装。
* `HTMLTestRunner.py`: 修改的HTMLTestRunner报告。
* `TestRunner.py`: 一个简单的 unittest运行器。

之后项目断断续续的在维护，直到2019年，也许是太闲了，加上对UI自动化有了更深入的理解，重新投入主要精力维护pyse项目。

后来就需要将提交到pypi，这样更方便通过`pip`安装，发现 pyse 已经被占用了，后来更名为`seldom`，其实命名没有太多寓意，就是看他长得和`selenium`比较接近。


2020年1月发布1.0版本，之所以发布1.0 是因为自认为框架的功能比较成熟了，并且花费时间补充了文档。大家都不重视文档，其实文档非常重要，也需要花大量的时间编写和维护。有时间你加个功能很简单，编写说明文档和使用示例就要花费等同的时间。

1.0 版本之后，项目核心围绕着 selenium API的封装 和 unittest框架扩展（seldom基于unittest）等。

2021年4月正式发布 2.0，集成requests, 正式支持http接口测试。起因是发现cypress支持http调用，哦，原来UI测试工具也可以去做接口，格局一下子打开了！如何在不影响现有selenium API的情况下集成requests是2.0考虑的重点。

2022年1月seldom项目正式在公司内部推广使用，当时我们做了几版的接口测试平台，平台的开发维护成本比较高，对于复杂的场景用例，编写成本不比框架简单；测试人员也苦平台久已（小白当然喜欢平台，懂点儿编程得测试，都不太愿意被平台束缚）。

因为在公司得到推广使用，seldom 明显进入了更加快速的迭代开发阶段。

## seldom 3.0 背景

seldom集成App测试是顺理成章的事情，早在几个月前我已经在公司项目中尝试 seldom + appium 进行App自动化测试。App自动化的维护成本确实比接口要高许多，这是由App本身的特点决定的，框架很难做到实质上的改变。

2020年10月seldom 3.0 beta发布，之所以选择appium有几个原因：

1. appium 是由商业工具在维护，历史比较长，不会随意停止维护。
2. appium 应用更加广泛，使用得人更多，支持得平台多（android/ios/flutter）
3. appium 继承selenium，对于seldom来说对原有API改动最小。

> 注：目前刚刚发布 seldom beta2 版本。

## seldom 简单示例

如果你熟悉appium 自动化测试环境，那么使用seldom 几乎不需要学习成本，他只是对`Appium-Python-Client` 的API做了简单的封装。

简单示例：

```py
# test_app.py
import seldom

class TestBBS(seldom.TestCase):

    def test_bbs_search(self):
        """BBS搜索测试 """
        self.click(id_="com.meizu.flyme.flymebbs:id/nw")
        self.type(id_="com.meizu.flyme.flymebbs:id/nw", text="flyme")
        self.click(id_="com.meizu.flyme.flymebbs:id/o1")
        self.sleep(2)
        elems = self.get_elements(id_="com.meizu.flyme.flymebbs:id/a29")
        for title in elems:
            self.assertIn("lyme", title.text)


if __name__ == '__main__':
    desired_caps = {
        'deviceName': 'JEF_AN20',
        'automationName': 'UiAutomator2',
        'platformName': 'Android',
        'platformVersion': '10.0',
        'appPackage': 'com.meizu.flyme.flymebbs',
        'appActivity': '.ui.LoadingActivity',
        'noReset': True,
    }
    seldom.main(app_info=desired_caps, app_server="http://127.0.0.1:4723")
```

运行日志：

```shell
> python .\test_app.py

              __    __
   ________  / /___/ /___  ____ ____
  / ___/ _ \/ / __  / __ \/ __ ` ___/
 (__  )  __/ / /_/ / /_/ / / / / / /
/____/\___/_/\__,_/\____/_/ /_/ /_/  v3.0.0beta1
-----------------------------------------
                             @itest.info


XTestRunner Running tests...

----------------------------------------------------------------------
2022-10-03 00:01:30 webdriver.py | INFO | 💤️ sleep: 5s.
2022-10-03 00:01:35 webdriver.py | INFO | ✅ Find 1 element: id=com.meizu.flyme.flymebbs:id/nw  -> click.
2022-10-03 00:01:36 webdriver.py | INFO | ✅ Find 1 element: id=com.meizu.flyme.flymebbs:id/nw  -> input 'flyme'.
2022-10-03 00:01:37 webdriver.py | INFO | ✅ Find 1 element: id=com.meizu.flyme.flymebbs:id/o1  -> click.
2022-10-03 00:01:37 webdriver.py | INFO | 💤️ sleep: 2s.
2022-10-03 00:01:39 webdriver.py | INFO | ✅ Find 5 element: id=com.meizu.flyme.flymebbs:id/a29 .
flyme的屏幕色彩显示应该是比较差的

魅族17的Flyme9状态栏下拉问题。

flyme9.3连上耳机来电话还是会外放

flyme自带录屏功能吗？

关于Flyme 8.18.0A稳定版


Generating HTML reports...
.12022-10-03 00:01:40 runner.py | SUCCESS | generated html file: file:///D:\github\seldom\reports\2022_10_03_00_01_23_result.html
2022-10-03 00:01:40 runner.py | SUCCESS | generated log file: file:///D:\github\seldom\reports\seldom_log.log
```

## AppiumLab 类

Lab即实验室的意思，在`AppiumLab` 类中对 appium 的一些API做了二次封装。


* __Action__

Action中提供基本滑动/触摸操作。

```py
from seldom.appium_lab import AppiumLab

appium_lab = AppiumLab(self.driver)
# 触摸坐标位
appium_lab.tap(x=100, y=200)
# 上划
appium_lab.swipe_up()
# 下划
appium_lab.swipe_down()
```

* __Switch__

Switch中提供基本上下文切换操作。
```python
from seldom.appium_lab import AppiumLab

appium_lab = AppiumLab(self.driver)

# 切换原生app
appium_lab.switch_to_app()
# 切换webview
appium_lab.switch_to_web()
# 切换flutter
appium_lab.switch_to_flutter()
```

*  __Find__

Find中提供基于文本的查找，一个元素可以没有ID、name，但一定有显示的文本，这里提供了一组基于文本的查找。
```python
from seldom.appium_lab import AppiumLab

appium_lab = AppiumLab(self.driver)

# Android
appium_lab.find_view(text="xxx标题").click()
appium_lab.find_view(content_desc="xxx标题").click()
appium_lab.find_edit_text(text="xxx标题").click()
appium_lab.find_button(text="xxx标题").click()
appium_lab.find_button(content_desc="xxx标题").click()
appium_lab.find_text_view(text="xxx标题").click()
appium_lab.find_image_view(text="xxx标题").click()
appium_lab.find_check_box(text="xxx标题").click()

# iOS
appium_lab.find_static_text(text="xxx标题").click()
appium_lab.find_other(text="xxx标题").click()
appium_lab.find_text_field(text="xxx标题").click()
appium_lab.find_image(text="xxx标题").click()
appium_lab.find_ios_button(text="xxx标题").click()
```

* __keyboard__

keyboard中提供基于键盘的输入和操作。
```
from seldom.appium_lab import AppiumLab

appium_lab = AppiumLab(self.driver)

# 基于键盘输入（支持大小写）
appium_lab.key_text("Hello123")
# 手机home键
appium_lab.home()
# 手机返回键
appium_lab.back()
# 判断当前虚拟键盘是否显示（True/False）
ret = appium_lab.is_keyboard_shown()
print(ret)
# 收起虚拟键盘
appium_lab.hide_keyboard()
```

## Page Object设计模式

在编写App自动化测试时，推荐使用page object models(简称 PO设计模式)。你可以看到seldom并没有完全封装appium的API，我们可以借助 poium 来实现基于元素的定位。

github: https://github.com/SeldomQA/poium

* 安装poium

```shell
> pip install poium
```

* 使用poium

在seldom中基于poium实现元素的定位和操作。

```py
import seldom
from poium import Page, Element, Elements


class BBSPage(Page):
    search_input = Element(id_="com.meizu.flyme.flymebbs:id/nw")
    search_button = Element(id_="com.meizu.flyme.flymebbs:id/o1")
    search_result = Elements(id_="com.meizu.flyme.flymebbs:id/a29")


class TestBBS(seldom.TestCase):

    def start(self):
        self.bbs_page = BBSPage(self.driver)

    def test_bbs(self):
        # 定义运行环境
        self.sleep(5)
        self.bbs_page.search_input.click()
        self.bbs_page.search_input.send_keys("flyme")
        self.bbs_page.search_button.click()
        elems = self.bbs_page.search_result
        for title in elems:
            print(title.text)
            self.assertIn("flyme", title.text.lower())
```

__定位方法__

poium 支持的定位方法。

```py
# selenium
css = "xx"
id_ = "xx"
name = "xx"
xpath = "xx"
link_text = "xx"
partial_link_text = "xx"
tag = "xx"
class_name = "xx"

# appium
ios_uiautomation = "xx"
ios_predicate = "xx"
ios_class_chain = "xx"
android_uiautomator = "xx"
android_viewtag = "xx"
android_data_matcher = "xx"
android_view_matcher = "xx"
windows_uiautomation = "xx"
accessibility_id = "xx"
image = "xx"
custom = "xx"
```

__Element类参数__

* timeout: 设置超时检查次数，默认为5。
* index: 设置元素索引，当你的定位方式默认匹配到多个元素时，默认返回第1个，即为0.
* describe: 设置元素描述，默认为undefined, 建议为每个元素增加描述。
