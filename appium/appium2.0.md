## appium 2.0 尝鲜

appium 创建了Appium 2.0的项目看板，项目正在开发中。

https://github.com/appium/appium/projects/2


### Appium 2.0 核心特性

* __独立的驱动__：能够安装和使用基于你的应用平台的解耦的驱动程序。(iOS, Android, Windows OS, Flutter, etc.) 

> 我们知道Appium为了支持多平台，集成了各种驱动在里面，使他变得比较笨重，我们在使用Appium的时候往往只完成一两个平台的测试，Appium 2.0 就可以按照需求去安装平台驱动。

例如，只做iOS测试，可以只安装xcuitest。

```
> appium driver install xcuitest
```

* __插件生态__: 能够通过插件和与其他技术的集成来修改Appium框架。

> 除了驱动可以根据需求安装，另外一些能力可以通过插件的方式提供安装。

例如，想使用报告插件，可以安装`appium-reporter-plugin`.

```
> appium plugin install --source=npm appium-reporter-plugin
```

### Appium 2.0 安装

* 升级npm 

npm 版本需要大于8.x。

```
> npm install -g npm
```

* 安装appium 

```shell
> npm install -g appium@next
```
这是全局的安装方式，如果你正在使用appium 1.x，可以创建一个目录，使用局部安装。

```shell
> npm install appium@next
```

* 检查版本

```shell
> appium --version
2.0.0-beta.43
```

* 查看驱动

```shell
> appium driver list

✔ Listing available drivers
- uiautomator2 [not installed]
- xcuitest [not installed]
- youiengine [not installed]
- windows [not installed]
- mac [not installed]
- mac2 [not installed]
- espresso [not installed]
- tizen [not installed]
- flutter [not installed]
- safari [not installed]
- gecko [not installed]
```

* 安装驱动

```shell
appium driver install uiautomator2
```

* 安装报告插件

```shell
> appium plugin install --source=npm appium-reporter-plugin
```


### appium 2.0 使用

* 使用插件的方式启动appium

```shell
> appium --use-plugins=appium-reporter-plugin
...
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
[Appium] Available drivers:
[Appium]   - espresso@2.8.3 (automationName 'Espresso')
[Appium]   - uiautomator2@2.4.7 (automationName 'UiAutomator2')
[Appium] Available plugins:
[Appium]   - gestures@1.0.0-beta.4
[Appium]   - appium-reporter-plugin@1.0.0-beta.7 (ACTIVE)
```

编写自动规划用例:

```python
# test_sample.py
import unittest
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy


class TestBBS(unittest.TestCase):

    def setUp(self):
        desired_caps = {
            'deviceName': 'JEF_AN20',
            'automationName': 'UiAutomator2',
            'platformName': 'Android',
            'platformVersion': '10.0',
            'appPackage': 'com.meizu.flyme.flymebbs',
            'appActivity': '.ui.LoadingActivity',
            'noReset': True,
        }

        self.dr = webdriver.Remote(
            command_executor='http://127.0.0.1:4723',
            desired_capabilities=desired_caps)

    def tearDown(self):
        self.dr.quit()

    def test_bbs(self):
        # 定义运行环境
        sleep(5)
        self.dr.find_element(MobileBy.ID, "com.meizu.flyme.flymebbs:id/nw").click()
        sleep(2)
        self.dr.find_element(MobileBy.ID, "com.meizu.flyme.flymebbs:id/nw").send_keys("flyme")
        self.dr.find_element(MobileBy.ID, "com.meizu.flyme.flymebbs:id/o1").click()
        sleep(2)

        title_list = self.dr.find_elements(MobileBy.ID, "com.meizu.flyme.flymebbs:id/a29")
        for title in title_list:
            print(title.text)
            self.assertIn("lyme", title.text)


if __name__ == '__main__':
    unittest.main()
```

* 运行测试

```shell
> python test_sample.py
```

__问题__

1. appium 服务地址：`http://127.0.0.1:4723`， 后面不要加:`/wd/hub`。
2. `appium-reporter-plugin` 插件从名字看是生成报告的，我们知道`测试报告`一定是和`测试框架`绑定的一个概念，事实告诉我没那么简单。

> appium-reporter-plugin assumes every test/spec uses new driver session. For commands invoked on the driver session, screenshot and metrics are captured at server side. At the end of the test i.e., before deleting the driver session, driver.setTestInfo(..) should be called to map test information. After all the tests are completed driver.getReport() can be called to fetch the html report and written to file.

时间原因，我也没再去倒腾~！插件地址：

https://github.com/AppiumTestDistribution/appium-reporter-plugin

