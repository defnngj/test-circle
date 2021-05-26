# 自动化测试工具taiko


## What’s Taiko?

Taiko 是一个免费和开源的浏览器自动化工具，由ThoughtWorks团队开发。Taiko是一个Node.js库，有一个清晰简洁的API来自动化基于Chromium的浏览器(Chrome, Microsoft Edge, Opera)和Firefox。用Taiko编写的测试可读性和可维护性都很高。

## Features

以下是它和其他自动化测试工具不同的特性。

* 安装简单
* 交互式记录器
* 智能的选择
* 可以处理XHR和动态内容
* Request/Response stubbing and mocking

## 安装

需要先安装Node.js，然后使用`npm` 命令。

```shell
> npm install -g taiko
```


## 交互模式

Taiko 提供了交互模式运行自动化测试。

```shell
❯ taiko

Version: 1.2.5 (Chromium: 88.0.4314.0)
Type .api for help and .exit to quit

> openBrowser()
[PASS] Browser opened

> goto("https://www.baidu.com")
[PASS] Navigated to URL https://www.baidu.com

> write("taiko")
[PASS] Wrote taiko into the focused element.

> click("百度一下")
[PASS] Clicked element matching text "百度一下"  1 times

> closeBrowser()
[PASS] Browser closed
>
```

首先，通过`taiko` 命令进入到taiko的交互模式。

然后，`goto()` 一个网站，常规的实现。

接下来，最神奇的地方在于我并没有编写定位方式，taiko就找到了搜索输入框并输入了“taiko”关键字。

继续 click() 一个叫“百度一下”的按钮。

最后，关闭浏览器。

## 元素定位

为了进一步验证taiko的智能定位，我们进入一个更复杂的页面

```shell
> openBrowser()
[PASS] Browser opened

> goto("https://seleniumbase.io/demo_page")
[PASS] Navigated to URL https://seleniumbase.io/demo_page

> write("taiko")
[FAIL] Error: Element focused is not writable, run `.trace` for more info.
```

这个页面有不止一个输入框，你会发现taiko并不能智能的定位到某个输入框，哪怕是按照顺序定位页面上的第一个。通过查看官方API，找到了定位方法。

```shell
> write("taiko", into(textBox({id: 'myTextInput'})))
[PASS] Wrote taiko into the textBox[id="myTextInput"]
```


## 学习API

taiko 的API非常清晰明了，如果你有自动化测试库的使用经验，应该很容易掌握。

https://docs.taiko.dev/api/reference/

当然，也可以在交互模式中查看API。

```shell
❯ taiko

Version: 1.2.5 (Chromium: 88.0.4314.0)
Type .api for help and .exit to quit

> .api    # 查看所有API

Browser actions
    openBrowser, closeBrowser, client, switchTo, intercept, emulateNetwork, emulateDevice, setViewPort, resizeWindow, openTab, closeTab, openIncognitoWindow, closeIncognitoWindow, overridePermissions, clearPermissionOverrides, setCookie, deleteCookies, getCookies, setLocation, clearIntercept

Page actions
    goto, reload, goBack, goForward, currentURL, title, click, doubleClick, rightClick, dragAndDrop, hover, focus, write, clear, attach, press, highlight, clearHighlights, mouseAction, scrollTo, scrollRight, scrollLeft, scrollUp, scrollDown, screenshot, tap, emulateTimezone

...

> .api click   # 查看某个API的说明和用法
Fetches an element with the given selector, scrolls it into view if needed, and then clicks in the center of the element. If there's no element matching selector, the method throws an error.

Parameters:

...

Examples:
        await click('Get Started')
        await click(link('Get Started'))
        await click({x : 170, y : 567})
        await click('Get Started', { navigationTimeout: 60000,  force: true })
        await click('Get Started', { navigationTimeout: 60000 }, below('text'))
        await click('Get Started', { navigationTimeout: 60000, position: 'right' }, below('text'))

> .exit   # 退出交互模式
```

### 生成脚本

我们完成一个稍微复杂一点的例子，进行一个搜索设置，设置搜索结果只显示中文。

```shell
> openBrowser()
[PASS] Browser opened
> goto("https://www.baidu.com")
[PASS] Navigated to URL https://www.baidu.com
> click("设置")
[PASS] Clicked element matching text "设置"  1 times
> click("搜索设置")
[PASS] Clicked element matching text "搜索设置"  1 times
> click("简体中文")
[PASS] Clicked element matching text "简体中文"  1 times
> click("保存设置")
Uncaught:
There is no handler registered for alert popup displayed on the page https://www.baidu.com/.
          This might interfere with your test flow. You can use Taiko's alert API to handle this popup.
          Please visit https://docs.taiko.dev/#alert for more details
> alert('已经记录下您的使用偏好', accept())
```

整个操作过程非常的爽，因为我全程不用关心`元素的定位方法`， 基本上看到什么就点击什么。

接下来，通过`.code` 命令将前面的操作过程生成脚本。

```shell
> .code
const { openBrowser, goto, click, alert, closeBrowser } = require('taiko');
(async () => {
    try {
        await openBrowser();
        await goto("https://www.baidu.com");
        await click("设置");
        await click("搜索设置");
        await click("简体中文");
        await click("保存设置");
        await alert('已经记录下您的使用偏好', accept());
    } catch (error) {
        console.error(error);
    } finally {
        await closeBrowser();
    }
})();

```

或者直接生成 `.js` 文件。

```shell
...
> .code baiduSetting.js  # 生成js文件
> .exit                  # 退出交互模式

D:/new_tech/taiko_pro via ⬢ v14.15.5 took 14m32s
❯ ls                     # 查看当前目录下的文件


    目录: D:\new_tech\taiko_pro


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----          2021/5/9     14:45            727 baiduSetting.js
```


### 运行脚本

真正使脚本可以运行，我做了适当的修改。

```js
const { openBrowser, goto, click, alert, closeBrowser } = require('taiko');
(async () => {
    try {
        await openBrowser({headless: false});
        await resizeWindow({width:1280, height:800})
        await goto("https://www.baidu.com");
        await click("设置");
        await click("搜索设置");
        await click("简体中文");
        await alert('已经记录下您的使用偏好', async () => await accept());
        await click("保存设置");
    } catch (error) {
        console.error(error);
    } finally {
        await closeBrowser();
    }
})();
```

* `{headless: false}`: 默认开启`true`，通过设置为`false`将其关闭，这样就可以看到浏览器的运行过程了。
* `resizeWindow()`: 设置浏览器的宽高。
* `alert()`: 在操作警告框之前，先要设置针对警告的操作，这一点有点反常识。

__运行脚本__

```
❯ npx taiko .\baiduSetting.js
[PASS] Browser opened
[PASS] Window resized to height 800 and width 1280
[PASS] Navigated to URL https://www.baidu.com
[PASS] Clicked element matching text "设置"  1 times
[PASS] Clicked element matching text "搜索设置"  1 times
[PASS] Clicked element matching text "简体中文"  1 times
[PASS] Accepted dialog
[PASS] Clicked element matching text "保存设置"  1 times
[PASS] Browser closed
```

__慢执行__

`--observe`参数在每个动作执行之前增加3秒的延迟，在测试页面上突出Taiko的API动作。

```
❯ npx taiko .\baiduSetting.js --observe
```

### 总结

学习过那么多UI自动化测试工具/框架，taiko真的有眼前一亮的感觉。Web UI自动化的痛点之一就是元素定位，taiko正在解决这个痛点，当然，解决的也不是非常完美，但在上面的例子中，编写自动化的过程还是非常爽的。