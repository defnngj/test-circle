# appium 文字识别插件之 OCR-plugin

> OCR（Optical Character Recognition，光学字符识别）是一种将图像或手写文本转换成可编辑文本的技术。它可以识别图像中的文字，并将其转换成计算机可识别的文本格式，从而实现自动化的文字识别和处理。

appium-ocr-plugin 是一个基于Tesseract的Appium OCR插件。它依赖Tesseract.js进行OCR处理。具备以下特点：

* 新的OCR端点：调用新的Appium服务器端点对当前截图进行OCR，并返回匹配的文本和元数据。
  
* OCR context：切换到OCR上下文，页面源将被更新以响应屏幕上找到的文本对象对应的XML。 

* 基于OCR文本查找元素：在OCR上下文中，使用XPath将根据页面源的OCR XML版本找到“元素”。然后以纯粹的屏幕位置为基础以最小的方式与这些找到的元素进行交互（click，getText）。

## 安装

安装Appium OCR plugin插件。

```bash
appium plugin install images--source=npm appium-ocr-plugin
```

查看已安装的Appium插件。

```bash
> appium plugin list --installed
✔ Listing installed plugins
- ocr@0.2.0 [installed (npm)]
```

启动Appium server时指定使用ocr插件。
```bash
> appium server --address '127.0.0.1' -p 4723  --use-plugins=ocr
```

创建OCR扩展脚本。

```py
# extension/orc_extension.py
from appium.webdriver.webdriver import ExtensionBase

# define an extension class
class OCRCommand(ExtensionBase):
    def method_name(self):
        return 'ocr_command'

    def ocr_command(self, argument):
        return self.execute(argument)['value']

    def add_command(self):
        add = ('post', '/session/$sessionId/appium/ocr')
        return add
```

创建OCRCommand继承ExtensionBase类，ExtensionBase用于将扩展命令定义为驱动程序的基类。`method_name()`方法定义方法名，`ocr_command()`方法用于实现方法名；`add_command()`方法用于添加命令。


## 使用OCR插件

编写App自动测试脚本。

```py
# appium_orc_demo.py
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from extension.ocr_extension import OCRCommand

capabilities = {
  ...
}

appium_server_url = "http://127.0.0.1:4723"
options = UiAutomator2Options().load_capabilities(capabilities)
driver = webdriver.Remote(command_executor=appium_server_url, options=options, extensions=[OCRCommand])
driver.implicitly_wait(10)

ocr = driver.ocr_command({})
print(ocr)
```

首先导入OCRCommand类，通过Remote类创建驱动的时候，通过extensions参数传入OCRCommand类。

调用ocr_command()方法（即OCRCommand类实现的方法）会对当前屏幕进行截图，并通过OCR技术识别图片中的文字。


## OCR识别对象

根据上面代码示例，打印ocr变量得到一个JSON结构体。

```json
{
  "words": [
    {
      "text": "mEngine", "confidence": 88.47775268554688,
      "bbox": {"x0": 86, "y0": 509, "x1": 308, "y1": 560}
    },
    {
      "text": "Flyme", "confidence": 91.3454818725586,
       "bbox": {"x0": 316, "y0": 1132, "x1": 420, "y1": 1172}
      },
    {
      "text": "A9", "confidence": 34.86248779296875,
      "bbox": {"x0": 1017, "y0": 2565, "x1": 1078, "y1": 2595}
    }
  ],
  "lines": [
    {
      "text": "mEngine BY Ni0vEh 1 Bl\n\n", "confidence": 21.003677368164062,
     "bbox": {"x0": 86, "y0": 500, "x1": 674, "y1": 560}
    },
    {
      "text": "Flyme\n\n", "confidence": 91.3454818725586,
     "bbox": {"x0": 316, "y0": 1132, "x1": 420, "y1": 1172}
    },
    {
      "text": "A9\n", "confidence": 34.86248779296875,
      "bbox": {"x0": 1017, "y0": 2565, "x1": 1078, "y1": 2595}
    }
  ],
  "blocks": [
    {
      "text": "mEngine BY Ni0vEh 1 Bl\n\n", "confidence": 21.003677368164062,
       "bbox": {"x0": 86, "y0": 500, "x1": 674, "y1": 560}
      },
    {
      "text": "Flyme\n\n", "confidence": 91.3454818725586,
      "bbox": {"x0": 316, "y0": 1132, "x1": 420, "y1": 1172}
    },
    {
      "text": "A9\n", "confidence": 34.86248779296875, 
      "bbox": {"x0": 1017, "y0": 2565, "x1": 1078, "y1": 2595}
    }
  ]
}
```

JSON结构体说明：

* wrods - Tesseract识别的单个单词的列表。

* lines - Tesseract识别的文本行的列表。

* blocks - Tesseract识别连续文本块的列表。

每项都引用一个OCR对象，它们本身包含3个数据：

* text：识别的文本。

* confidence：Tesseract对于给定文本的OCR处理结果的置信度（范围在0到100之间）。

* bbox：发现文本的边界框，“边界框”标记为x0、x1、y0和y1的值的对象。分别表文本的上下左右坐标位置，其中。这里，x0表示发现文本的左边x坐标，x1表示右边x坐标，y0表示上部y坐标，y1表示下部y坐标。

## 查找与操作元素


当通过OCR技术识别出来了一些文本，并且知道这些文本的置信度和坐标位，接下来就是使用文本定位元素了，分两步：

1. 切换OCR上下文。

2. 通过xpath定位元素，并对其进行操作。


![](app-bbs.png)


示例代码如下：

```py
# appium_orc_demo.py
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from extension.ocr_extension import OCRCommand

capabilities = {
    ...
}

appium_server_url = "http://127.0.0.1:4723"
options = UiAutomator2Options().load_capabilities(capabilities)
driver = webdriver.Remote(command_executor=appium_server_url, options=options, extensions=[OCRCommand])

driver.implicitly_wait(10)

ocr = driver.ocr_command({})
print(ocr)

driver.switch_to.context('OCR')
driver.find_element(AppiumBy.XPATH, '//words/item[text() = "Flyme"]').click()
```

使用switch_to.context()方法切换到OCR上下文。然后，使用xpth方式定位元素，其中`words`从单词列表中选取文本，`item`表示某一项，`text()="Flyme"`表示文本等于“Flyme”关键字。

