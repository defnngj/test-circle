## appium基于openv4node图像识别进行自动化测试

App自动化测试在面临元素定位时要比Web复杂很多，除了原生应用、MWeb应用、混合应用之外，还有flutter的逐渐流行，而且很多老的App都是部分内嵌flutter页面，这又给App自动化定位进一步增加了难度，图像识别是一个很好的方向；可以有效屏蔽页面元素属性。

Appium 在`V1.9.0`版本中提供了针对于图像识别的全新图片元素定位的方法。

### 安装列表

先来罗列要安装的工具，有点多~！

__安装基础__

> 这部分不会重点介绍，请自行准备。

* windows 11
* node.js/npm
* python
* chocolatey
* Android SDK
* Java 11
* Android设备一台

__安装工具__

> 本文偏重介绍一下工具的安装。

* appium
* appium-doctor
* cmake
* windows-build-tools
* chocolatey
* OpenCV
* opencv4nodejs
* python-client(appium)

### 安装工作

以下需要用到命令的，请以管理员权限在`windows PowerShell`下执行。


####  安装appium

使用appium 有两种方式，`appium`命令 和 `appium-desktop`，这里我们安装和使用前者。

```shell
> npm install -g appium
```

<br>

####  安装Cmake

OpenCV 使用 Cmake 来构建工程, 下载编译后的文件即可。

下载地址：https://github.com/Kitware/CMake/releases/


下载完后解压到任意路径，例如：`D:\appium\`，在环境变量中path添加 Cmake 的 bin 目录

- `D:\appium\cmake-3.23.1-windows-x86_64\bin` -> 添加环境变量Path。

<br>

####  安装 windows-build-tools

Build Tools 即构建工具，用于把源代码生成可执行应用程序的过程自动化的程序（例如Android app生成apk）。构建包括编译、连接等，把代码打包成可用的或可执行的形式。


```shell
> npm install --g windows-build-tools
```
安装过程会下载和安装`python27`，安装路径如下：`C:\Users\{user}\.windows-build-tools\python27`


- `C:\Users\fnngj\.windows-build-tools\python27` -> 添加环境变量Path。

<br>

####  安装OpenCV

```shell
> choco install OpenCV -y -version 4.5.0
```

choco 是windows下面的包管理工具。

OpenCV默认安装路径：`C:\tools\opencv\`


* 配置环境变量

新建系统变量：

```
变量名：OPENCV_BIN_DIR 变量值：C:\tools\opencv\build\x64\vc15\bin
变量名：OPENCV_DIR 变量值：C:\tools\opencv\build\x64\vc15
变量名：OPENCV_INCLUDE_DIR 变量值：C:\tools\opencv\build\include
变量名：OPENCV_LIB_DIR 变量值：C:\tools\opencv\build\x64\vc15\lib
```

* `%OPENCV_BIN_DIR%` -> 添加到环境变量path


####  安装opencv4nodejs

* 设置环境变量

```shell
> set OPENCV4NODEJS_DISABLE_AUTOBUILD=1
```

* 安装opencv4nodejs

```
> npm i -g opencv4nodejs
```

####  安装appium-doctor

appium-doctor用于检查appium安装环境。通过`npm`安装。

```
> npm i -g appium-doctor
```

* 检查appium环境。
  
```shell
> appium-doctor

info AppiumDoctor Appium Doctor v.1.16.0
info AppiumDoctor ### Diagnostic for necessary dependencies starting ###
info AppiumDoctor  ✔ The Node.js binary was found at: D:\Program Files\nodejs\node.EXE
info AppiumDoctor  ✔ Node version is 14.18.1
info AppiumDoctor  ✔ ANDROID_HOME is set to: D:\android\Sdk
info AppiumDoctor  ✔ JAVA_HOME is set to: C:\Program Files\Java\jdk-11.0.15
info AppiumDoctor    Checking adb, android, emulator
info AppiumDoctor      'adb' is in D:\android\Sdk\platform-tools\adb.exe
info AppiumDoctor      'android' is in D:\android\Sdk\tools\android.bat
info AppiumDoctor      'emulator' is in D:\android\Sdk\emulator\emulator.exe
info AppiumDoctor  ✔ adb, android, emulator exist: D:\android\Sdk
info AppiumDoctor  ✔ 'bin' subfolder exists under 'C:\Program Files\Java\jdk-11.0.15'
info AppiumDoctor ### Diagnostic for necessary dependencies completed, no fix needed. ###
info AppiumDoctor
info AppiumDoctor ### Diagnostic for optional dependencies starting ###
info AppiumDoctor  ✔ opencv4nodejs is installed at: C:\Users\fnngj\AppData\Roaming\npm. Installed version is: 5.6.0
info AppiumDoctor Bye! Run appium-doctor again when all manual fixes have been applied!
info AppiumDoctor
```

看到 `opencv4nodejs` 前面 √ 即可。


### 进行自动化测试


####  安装 python-client


appium支持不同语言的client编写自动化测试用例。这里以python的 python-client为例。

https://github.com/appium/python-client

```shell
> pip install Appium-Python-Client
```

####  启动 appium

```
> appium

[Appium] Welcome to Appium v1.22.3
[Appium] Appium REST http interface listener started on 0.0.0.0:4723
```

####  编写自动化用例

以某app为例，右下角悬浮的按钮很难定位，可以截图保存。

界面：

![](./meizu.png)

按钮截图：

![](./write.png)

保存路径为：`D:\appium\image\write.png`

编写自动规划用例

```python
from time import sleep
from appium import webdriver


# 定义运行环境
desired_caps = {
    'deviceName': 'JEF_AN20',
    'automationName': 'appium',
    'platformName': 'Android',
    'platformVersion': '10.0',
    'appPackage': 'com.meizu.flyme.flymebbs',
    'appActivity': '.ui.LoadingActivity',
    'noReset': True,
    'ignoreHiddenApiPolicyError': True
}

# 启动App
dr = webdriver.Remote(
    command_executor='http://127.0.0.1:4723/wd/hub',
    desired_capabilities=desired_caps)

sleep(2)

# 通过图片定位元素
dr.find_element_by_image(r"D:\appium\image\write.png").click()

```

## 总结

本文简单总结了整个安装过程，在这个过程中必定会踩不少坑，比如npm安装很慢 或 报错。缺少相关依赖。android SDK如何安装。需要一些相关的知识储备。

祝你好运，我的老伙计~！
