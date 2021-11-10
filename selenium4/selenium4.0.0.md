# selenim 4.0.0 发布

我们非常高兴地宣布Selenium 4的发布。这适用于Java、.net、Python、Ruby和Javascript。你可以从你最喜欢的包管理器或GitHub下载它!

https://github.com/SeleniumHQ/selenium/releases/tag/selenium-4.0.0


如果您已经是一个Selenium用户，那么这个更新应该很简单，只需改变依赖从`3.x`切换`4.0.0`即可。我们一直在努力确保这是一个`无痛`升级，重点是保持公共API尽可能稳定。

当然，我们已经做了一些更改，所以如果您依赖于那些标记为Selenium内部的代码，或者那些已弃用的代码，那么您可能会遇到一些问题。请查看我们的文档，了解如何处理我们所知道的每个常见问题。

https://www.selenium.dev/documentation/getting_started/how_to_upgrade_to_selenium_4/


Selenium4 不仅仅是一个稳定的版本！它带来了一大堆新的和令人兴奋的特性，我们希望这些特性将使您的测试编写起来更加有趣！运行时更稳定！让我们来看看其中的一些新功能!

## 相对定位器

我们已经介绍了`相对定位器`。它们允许您使用人们也使用的语言指定在页面上可以找到元素的位置；比如`在那个元素之上`，或者`在另一个元素的右边`。这将为您提供一种工具来应对复杂定位器，使您的测试读起来更清楚一些，并更能适应页面DOM的变化。我们不是第一个想到这个主意的人——这个荣誉属于`Sahi`(注：Sahi一款web自动化工具)——但如果你以前没有用过，我们希望你喜欢!

```py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with

passwordField = driver.find_element(By.ID, "password")
emailAddressField = driver.find_element(locate_with(By.TAG_NAME, "input").above(passwordField))

```

`above()` 用于要查找的元素在`指定元素`的上方。


## 基于Firefox/Chromium的新功能

如果你使用的是火狐或源自于Chromium的浏览器，我们也增加了一大堆新功能。这些方法包括处理`“基本”和“摘要”身份验证`；网络监听(Are you an HTTP 418?)；以及执行常见请求的任务，如`等待DOM的更新`，或提供查看Javascript错误的方法。

* 认证

```js
const {Builder} = require('selenium-webdriver');

(async function example() {
  try {
    let driver = await new Builder()
      .forBrowser('chrome')
      .build();

    const pageCdpConnection = await driver.createCDPConnection('page');
    await driver.register('username', 'password', pageCdpConnection);
    await driver.get('https://the-internet.herokuapp.com/basic_auth');
    await driver.quit();
  }catch (e){
    console.log(e)
  }
}())
```

> 注：python 没有`register()` 方法，目前还不确定是否为bug。


* Are you an HTTP 418?

> 这就是个玩笑。IETF在1998年愚人节时发布的一个笑话RFC，具体可以参考RFC 2324 - Hyper Text Coffee Pot Control Protocol (HTCPCP/1.0)超文本咖啡壶控制协议。htcpcp1.0协议中的418的意义是：当客户端给一个茶壶发送泡咖啡的请求时，茶壶就返回一个418错误状态码，表示"我是一个茶壶" 或者 "我是个杯具"。

* 等待DOM的更新

```js
const {Builder, until} = require('selenium-webdriver');
const assert = require("assert");

(async function example() {
  try {
    let driver = await new Builder()
      .forBrowser('chrome')
      .build();

    const cdpConnection = await driver.createCDPConnection('page');
    await driver.logMutationEvents(cdpConnection, event => {
      assert.deepStrictEqual(event['attribute_name'], 'style');
      assert.deepStrictEqual(event['current_value'], "");
      assert.deepStrictEqual(event['old_value'], "display:none;");
    });

    await driver.get('dynamic.html');
    await driver.findElement({id: 'reveal'}).click();
    let revealed = driver.findElement({id: 'revealed'});
    await driver.wait(until.elementIsVisible(revealed), 5000);
    await driver.quit();
  }catch (e){
    console.log(e)
  }
}())
```

我们以一种与现有api相适应的方式添加了这些新特性。没有必要重写您的测试:只要在您觉得合适的时候使用新特性即可。

## Selenium Grid

我们还重建了Selenium Grid，借鉴了Zalenium和Selenoid等成功项目的经验，以增强其能力。这个新的Grid就像在传统的`Hub`和`Node`配置中一样，可以在单台机器上运行单个进程，但它也支持完全分布式模式，用于运行Kubernetes的现代基础设施。它具有更好的内置安全性，因为我们知道保护Grid可能是一项困难的任务。在所有这些规模和大小，我们添加到语言绑定的所有新特性都将按照预期工作。

Grid还可以管理本地机器上的Docker容器，拉出独立的firefox服务器之类的图像，这样您的基础设施维护就会稍微轻松一些。

最后，Grid更容易管理。我们修改了UI，将其置于GraphQL模型之上，任何人都可以自由查询并使用它来创建自己的Grid可视化或监视器。如果您想查看正在运行的会话，可以打开并与之交互的实时VNC(虚拟网络计算机)预览，从而更好地了解正在发生的事情。如果你想要更多的信息，我们已经在网格中集成了对OpenTelemetry的支持，所以现在你可以确切地知道发生了什么，在哪里，什么时候。


## 感谢

我知道说这是一种“非常愉快”的陈词滥调，但说实话，这是真的。开发这个新版本的Selenium是一个与一些了不起的工程师一起工作的机会，也是一个充满活力和活力的社区的一部分。与这些人一起编写这些代码非常有趣，在这里向尽可能多的人说“谢谢”感觉是正确的。所以，不用再等了。

## 最后

本文试着对《Announcing Selenium 4》进行了简单的翻译，本来怀着激动的心情来的，结果当我一一验证这些新特性的时候，非常糟糕！这特么就是打磨这么久出的 4.0 正式版。

1. python（Selenium）API缺失。
2. 官方文档的例子不完整，还有错误。

https://github.com/SeleniumHQ/selenium/issues/9912
