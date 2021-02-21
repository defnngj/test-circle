# 为什么选择Playwright?

Playwright可以在所有浏览器中实现快速、可靠和强大的自动化测试。这里将介绍Playwright的特点，以便于帮助你快速的了解Playwright。

* 支持所有浏览器
* 快速可靠的执行
* 强大的自动化功能
* 与你的工作流集成

## 支持所有浏览器

* 在Chromium, Firefox 和 WebKit上运行测试：Google Chrome和Microsoft Edge都是基于Chromium项目，Apple Safari基于WebKit，还有Mozilla 的Firefox。

```js
const { chromium, webkit, firefox } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  // const browser = await webkit.launch();
  // const browser = await firefox.launch();

  const page = await browser.newPage();
  await page.goto('http://www.baidu.com/');
  await page.screenshot({ path: `example.png` });
  await browser.close();
})();
```

> 扩展：
> WebKit是Apple开源的浏览器引擎，Apple Safari就是基于WebKit开发。Chromium是开源浏览器项目，早期使用的也是WebKit内核，后来在WebKit的基础上fork了一个分支叫Blink，然后自己维护。

* 测试移动端：通过设置驱动模式可以模拟移动浏览器的效果。

```js
const { webkit, devices } = require('playwright');
const iPhone11 = devices['iPhone 11 Pro'];

(async () => {
  const browser = await webkit.launch();
  const context = await browser.newContext({
    ...iPhone11,
    locale: 'en-US',
    geolocation: { longitude: 12.492507, latitude: 41.889938 },
    permissions: ['geolocation']
  });
  const page = await context.newPage();
  await page.goto('https://m.baidu.com');
  await page.screenshot({ path: 'colosseum-iphone.png' });
  await browser.close();
})();
```

* Headless 和 headful: Playwright支持所有平台和浏览器上使用Headless模式和Headful模式。Headful非常适合调试。Headless运行更快，也可以更方便的在CI/云平台上运行。

```js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({headless: false});
  // ...
})();
```
`headless` 默认开启，设置为false，即为 headful模式，可以看到自动化的过程。


## 快速可靠的执行

* 自动等待: Playwright 可以自动等待元素，这将会提高自动化的稳定性，简化测试的编写。
* 浏览器上下文并行：对具有浏览器上下文的多个并行、隔离的执行环境，重用单个浏览器实例。

```js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({headless: false, slowMo: 50 });
  const context = await browser.newContext();
  const page = await context.newPage();
  await page.goto('http://www.testpub.cn/login');
  await page.fill("#inputUsername", 'admin');
  await page.fill("#inputPassword", 'admin123456');
  await page.click('"Sign in"');
  await page.close();

  const page2 = await context.newPage();
  await page2.goto("http://www.testpub.cn/guest_manage/")
  await browser.close();
})();
```

我来解释一下，比如第一条用例执行了登录，第二条用例直接通过上下文创建一个新的页面去执行登录之后的功能，即保证了用例的相对独立性，又减少了用例的重复操作。

* 有弹性的选择元素：Palywright可以依赖面向用户的字符串，如文本内容和可访问性标签来选择元素。这些字符串比与DOM结构紧密耦合的选择器更有弹性。

```html
<button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
```
例如上面的元素一看就不太好定位，用户到的是一个按钮，名字叫`Sign in`，那么可以用这个定位方式。

```js
await page.click('"Sign in"');
```

## 强大的自动化能力

* 支持多个域、页面和表单： Palywright是一个 进程外（out-of-process） 自动化驱动程序，它不受页内JavaScript执行范围的限制，可以自动处理多个页面的场景。

```js
// Create two pages
const pageOne = await context.newPage();
const pageTwo = await context.newPage();

// Get pages of a brower context
const allPages = context.pages();
```

* 强大的网络控制： Palywright引入上下文范围的网络拦截存根和模拟网络请求。

```js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({headless: false, slowMo: 50 });
  const context = await browser.newContext({ acceptDownloads: true });
  const page = await context.newPage();
  await page.goto('https://pypi.org/project/selenium/#files');
  const [ download ] = await Promise.all([
    page.waitForEvent('download'), 
    page.click('#files > table > tbody > tr:nth-child(2) > th > a')
  ]);
  const path = await download.path();
  console.log("path", path);
  await browser.close();
})();
```

在 HTTP 认证，文件下载、网络请求响应方面都有很强的控制能力。

* 覆盖所有场景的功能：支持文件下载、上传，进程外表单，输入、点击，甚至是手机上流行的暗黑模式。

```js
// Create context with dark mode
const context = await browser.newContext({
  colorScheme: 'dark' // or 'light'
});
```

## 与你的工作流程集成

* 一行命令安装：运行`npm i playwright` 自动下载浏览器依赖，让你的团队快速上手。
* 支持TypeScript：Playwright 附带内置的自动完成类型和其他收益。
* 调试工具：通过 VS Code 完成自动化的调试。
* 语言绑定：Playwright 支持多种编程语言，这个前面的文章有介绍。
* 在CI上部署测试：你要可以使用Docker镜像，Playwright默认也是headless模式，你可以在任何环境上执行。