## App UI 自动化测试库

App移动端测试是个很大的话题，首先 区分 Android 和 iOS ，以及 harmonyos 平台，每个平台下都有自己的自动化测试工具。自动化工具又区分 调试工具、monkey 工具、UI自动化工具。


### AndroidX Test

AndroidX Test 是一组 Jetpack 库，可让您针对 Android 应用运行测试。AndroidX Test 提供 JUnit4 规则来启动 Activity 并在 JUnit4 测试中与它们交互。 它还包含 UI 测试框架，例如 Espresso、UI Automator 和 Robolectric 模拟器。


#### Robolectric

Robolectric 会模拟 Android 4.1（API 级别 16）或更高版本的运行时环境，并提供由社区维护的虚假对象（称为“影子”）。通过此功能，您可以测试依赖于框架的代码，而无需使用模拟器或模拟对象。Robolectric 支持 Android 平台的以下几个方面：

* 组件生命周期
* 事件循环
* 所有资源

官方文档：https://robolectric.org/


#### Espresso

Espresso 来编写简洁、美观且可靠的 Android 界面测试。Espresso 适用于编写Android中型测试 和 大型测试。


Espresso 还支持在大型测试中完成以下任务时实现同步：

* 完成跨应用的进程界限的工作流。仅适用于 Android 8.0（API 级别 26）及更高版本。

* 跟踪应用中长时间运行的后台操作。

* 执行设备外测试。

在线文档：https://developer.android.com/training/testing/espresso


#### UI Automator

UI Automator 是一个 UI 测试框架，适用于跨系统和的跨应用程序功能 UI 测试。它适用于大型测试，把Android和应用当成一个黑盒来测试。

UI Automator 测试框架的主要特性包括：

* 用于检索状态信息并在目标设备上执行操作的API。

* 支持跨应用UI测试的API。

在线文档：https://developer.android.com/training/testing/other-components/ui-automator


### adb

Android 调试桥 (adb) 是一种功能多样的命令行工具，可让您与设备进行通信。

它是一种客户端-服务器程序，包括以下三个组件：

* 客户端：用于发送命令。客户端在开发机器上运行。您可以通过发出 adb 命令从命令行终端调用客户端。

* 守护程序 (adbd)：用于在设备上运行命令。守护程序在每个设备上作为后台进程运行。

* 服务器：用于管理客户端与守护程序之间的通信。服务器在开发机器上作为后台进程运行。

在线文档：https://developer.android.com/studio/command-line/adb


### iOS 测试库

### XCTest


XCTest 用于iOS 移动应用程序测试，为Xcode项目创建并运行单元测试、性能测试和UI测试。兼容 XCode 5.0+。

XCTest的主要特性：

* XCTest是一个强大的iOS测试框架，可用于单元测试、性能测试和UI测试

* 无需安装：Xcode提供了使用XCTest开始移动自动化测试的环境。

* XCTest提供了对持续集成设施的良好控制

* XCTest允许用户界面记录和增强。

在线文档：https://developer.apple.com/documentation/xctest


### XCUITest

XCUITest 是一个用于执行 iOS 自动化测试的自动化 UI 测试框架。 它集成在 XCTest（Apple 的 Xcode 集成测试框架）工具中。

https://developer.apple.com/documentation/xctest/user_interface_tests

---

### iOS db(iOS debug bridge)

#### faceback idb

idb（iOS Development Bridge）是一个灵活的命令行界面，用于自动化 iOS 模拟器和设备。

官方地址：https://fbidb.io/

#### go-iOS

go-iOS是 iOS 设备功能的操作系统独立实现。可以使用它运行 UI 测试、启动或终止应用程序、安装应用程序等。

项目地址：https://github.com/danielpaulus/go-ios

#### sib

sib (Sonic iOS Bridge) 基于usbmuxd的iOS调试工具。

项目地址：https://github.com/SonicCloudOrg/sonic-ios-bridge

项目地址：

#### tidevice

tidevice（taobao iOS device）工具能够用于与iOS设备进行通信.

项目地址：https://github.com/alibaba/taobao-iphone-device

---

### appium

Appium 是一个开源项目和相关软件生态系统，旨在促进许多应用程序平台的 UI 自动化，包括移动（iOS、Android、Tizen）、浏览器（Chrome、Firefox、Safari）、桌面（macOS、Windows）、电视 （Roku、tvOS、Android TV、三星）等等。

#### appium

适用于基于 W3C WebDriver 协议构建的各种应用程序的跨平台自动化框架

项目地址：https://github.com/appium/appium


#### appium inspector


appium inspector 是由appium提供的移动应用程序的GUI检查器，帮助用户查看 app元素属性。

项目地址：https://github.com/appium/appium-inspector


#### python/java/ruby/c# client

appium 支持基于多种语言编写 appium 自动化测试脚本，为此，appium 推出了不同版本的 client 端口。

python-client: https://github.com/appium/python-client
java-client: https://github.com/appium/java-client
ruby-client: https://github.com/appium/ruby_lib
c#-client: https://github.com/appium/dotnet-client

#### WebDriverAgent

WebDriverAgent 是适用于 iOS 的 WebDriver 服务器实现，可用于远程控制 iOS 设备。它通过链接XCTest.framework并调用Apple的API直接在设备上执行命令来工作。

该项目由 facebook 开源，目前，facebook已经停止了对该项目的维护，appium fork 了分支，WebDriverAgent在appium得到了很好的持续维护。

项目地址：https://github.com/appium/WebDriverAgent

---

### AirtestProject

AirtestProject是网易游戏推出的自动化测试框架。 

#### airtest 

Airtest基于图像识别的跨平台UI自动化测试框架。适用于游戏和应用程序，支持的平台是Windows, Android和iOS。

项目地址：https://github.com/AirtestProject/Airtest

#### Poco

Poco是一个基于UI控件识别的自动化测试框架。目前支持Unity3D/cocos2dx-/Android原生应用/iOS原生应用/微信applet。在其他引擎中，你也可以通过访问poco-sdk来使用poco。

项目地址：https://github.com/AirtestProject/poco

#### AirtestIDE

Airtest IDE是一个跨平台的UI自动化测试编辑器，它有内置的Airtest和Poco插件功能，可以让你快速轻松地编写`Airtest`和`Poco`代码。

下载地址：http://airtest.netease.com/changelog.html

#### iOS-Tagent

iOS-Tagent是一个基于facebook WebDriverAgent的项目的分支，用于适配 Airtest 支持 iOS App 自动化测试。

项目地址：https://github.com/AirtestProject/iOS-Tagent

---

### openatx

openatx 提供了一组工具来支持移动自动化测试。

#### uiauotmator2

uiautomator2 是基于 Android 的 UI Automator库实现的 Python测试库。

UI Automator 是Google提供的用来做安卓自动化测试的一个Java库，基于Accessibility服务。原理是在手机上运行了一个http rpc服务，将UI Automator中的功能开放出来，然后再将这些http接口封装成Python库。


项目地址：https://github.com/openatx/uiautomator2

#### facebook-wda / wdapy

facebook-wda 是基于 facebook WebDriverAgent 实现的python 测试库。

由于facebook-wda 存在一些无法修复的历史遗留问题，作者重新创建了 wdapy 项目，希望在这个项目中解决遗留的问题。

项目地址：https://github.com/openatx/facebook-wda
项目地址：https://github.com/openatx/wdapy

> 注： facebook-wda/wdapy 需要借助 WebDriverAgent 进行自动化测试。


#### adbutils

adbutils 用于实现 adb 工具的 python 库。 adb 是Android 自带命令行工具，adbutils的命令的基础上包了一层，使用户可以通过python语言实现 adb的命令。


### maestro 

Maestro 是为您的移动应用程序自动化 UI 测试的最简单方法。

Maestro 建立在其前身（Appium、Espresso、UIAutomator、XCTest）的学习基础上。

* 内置耐剥落性能。UI元素并不总是在你期望的地方，屏幕点击并不总是通过，等等。Maestro接受了移动应用程序和设备的不稳定性，并试图对抗它。

* 内置的延迟容忍度。不需要在测试中添加sleep()调用。Maestro知道它可能需要时间来加载内容(即通过网络)，并自动等待它(但不会超过所需的时间)。

* 极其快速的迭代。测试是解释的，不需要编译任何东西。Maestro能够持续监视您的测试文件并重新运行它们

官方网站：https://maestro.mobile.dev/

### app Monkey 测试工具

#### fastbot

Fastbot 是一种基于模型的测试工具，用于对 GUI 转换进行建模以发现应用程序稳定性问题。 它结合了机器学习和强化学习技术，以更智能的方式帮助发现。

fastbot-android: https://github.com/bytedance/Fastbot_Android

fastbot-iOS: https://github.com/bytedance/Fastbot_iOS

#### App性能分析工作台

AnyTrace 是一款运行在PC桌面端的、用于线下分析移动端 Android/iOS 应用的性能、测评、专项分析的工具。目前主要提供了App 的性能指标评测、fastbot稳定性压测、内存、CPU、卡顿、启动等专项性能归因分析，以及一些常用的、实用的调试类工具集合。

在线文档：https://www.volcengine.com/docs/6431/82895


