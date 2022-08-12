## Monkey工具之fastbot-Android实践

## 背景

目前移动端App上线后 crash 率比较高，我们需要一款Monkey工具测试App的稳定性，更早地发现crash问题并修复。

前面一篇文章已经介绍过了fastbot-iOS的使用，文本将介绍 fastbot-android。

### 环境安装

准备工具：
- adb工具
- fastbot_Android: github地址：https://github.com/bytedance/Fastbot_Android

1. 克隆fastbot_Android 项目到本地。

```shell
> git clone https://github.com/bytedance/Fastbot_Android
```

1. 连接Android 设备，通过`adb`工具把相关文件push到Android 设备

```shell
> cd Fastbot_Android
> ll
-rw-r--r--   1 tech  staff   2.0K Jan 24 18:36 LICENSE
-rw-r--r--   1 tech  staff   4.7K Jan 24 18:36 README.md
drwxr-xr-x   3 tech  staff    96B Dec 21 11:57 data
drwxr-xr-x  16 tech  staff   512B Dec 21 11:58 doc
-rw-r--r--   1 tech  staff    84K Dec 21 11:58 fastbot-thirdpart.jar
-rwxr-xr-x   1 tech  staff   1.1M Dec 21 11:58 framework.jar
-rw-r--r--   1 tech  staff    17K Dec 21 11:58 handbook-cn.md
drwxr-xr-x   6 tech  staff   192B Dec 21 11:58 libs
-rw-r--r--   1 tech  staff    76K Dec 21 11:58 monkeyq.jar
drwxr-xr-x  12 tech  staff   384B Dec 21 11:58 test

> adb push *.jar /sdcard
fastbot-thirdpart.jar: 1 file pushed. 3.9 MB/s (85664 bytes in 0.021s)
framework.jar: 1 file pushed. 34.0 MB/s (1149240 bytes in 0.032s)
monkeyq.jar: 1 file pushed. 15.9 MB/s (77976 bytes in 0.005s)
3 files pushed. 19.1 MB/s (1312880 bytes in 0.065s)

> adb push libs/* /data/local/tmp/
libs/arm64-v8a/: 1 file pushed. 34.9 MB/s (1993400 bytes in 0.055s)
libs/armeabi-v7a/: 1 file pushed. 34.3 MB/s (1652716 bytes in 0.046s)
libs/x86/: 1 file pushed. 35.7 MB/s (2111484 bytes in 0.056s)
libs/x86_64/: 1 file pushed. 35.8 MB/s (2169816 bytes in 0.058s)
4 files pushed. 34.5 MB/s (7927416 bytes in 0.219s)
```

## 运行测试

1. 查看设备ID

```shell
> adb devices
List of devices attached
UMXDU20813000084        device
```

2. 运行fastbot

```shell
> adb -s UMXDU20813000084 shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p com.xxx --agent reuseq --running-minutes 60 --throttle 500 -v -v
```

__参数说明__

- -s  :  指定设备ID（可以通过adb 命令查看当前电脑接入的设备信息）。
- -p :  指定运行的App 包名（com.xxx）.
- --agent reuseq  : 遍历模式，无需更改。
- --runing-minutes :  遍历时长。
- --throttle :  遍历事件频率，建议为 500ms - 800ms
- --bugreport : 可选参数，崩溃时保存bug report log.
- --output-directory /sdcard/xxx :  log/carsh 另存目录。


## Crash、ANR捕捉

- Crash: 应用崩溃。

Fastbot 捕获到的Java Crash、ANR、Nativie Crash 会以追加的方式写入/sdcard/crash-dump.log 文件。

```shell
> adb shell  # 执行adb shell 进入手机系统
HWJEF:/ $ cd sdcard
HWJEF:/sdcard $ cat crash-dump.log  # 查看崩溃日志文件。
```

- ANR全称：Application Not Responding，也就是应用程序无响应。
fastbot  捕获的ARN 同时也会写入 /sdcard/oom-traces.log 文件。

```shell
> adb shell  # 执行adb shell 进入手机系统
HWJEF:/ $ cd sdcard
HWJEF:/sdcard $ cat crash-dump.log  # 查看无响应日志文件。
```


## Activity 覆盖率统计

Activity 是Android 应用中的概念，一般开发过程中一个Activity 对应一个页面，当然具体要看开发如何设计，一个Activity 也可以对应多个页面。
正常跑完Fastbot会在当前shell中打印totalActivity（总activity列表），ExploredActivity（遍历到的activity列表）以及本次遍历的总覆盖率。

- 总覆盖率计算公式： coverage = testedActivity / totalActivities * 100


> totalActivities：通过framework接口 PackageManager.getPackageInfo 获取，这包含app中所有的Activity，其中也包含了很多废弃、不可见、不可达等Activity。


## 自定义输入法

- 需求：遇到输入框，自定义输入关键字 。

- 准备： ADBKeyBoard 输入法

```shell
❯ git clone https://github.com/senzhk/ADBKeyBoard  # 克隆项目
Cloning into 'ADBKeyBoard'...
remote: Enumerating objects: 259, done.
remote: Counting objects: 100% (56/56), done.
remote: Compressing objects: 100% (38/38), done.
remote: Total 259 (delta 16), reused 15 (delta 2), pack-reused 203
Receiving objects: 100% (259/259), 924.98 KiB | 1.29 MiB/s, done.
Resolving deltas: 100% (74/74), done.

> cd ADBKeyBoard  # 进入项目目录

> ls
ADBKeyboard.apk      build.gradle         gradlew.bat          proguard-project.txt
LICENSE              gradle               ic_launcher-web.png  project.properties
README.md            gradlew              keyboardservice      settings.gradle

❯ adb install ADBKeyboard.apk  # 安装文件到手机上
Performing Streamed Install
Success
```

1. 输入随机字符串

配置`max.config` 配置文件（注：文件名字不可更改）。
https://github.com/bytedance/Fastbot_Android/blob/main/test/max.config

```conf
max.randomPickFromStringList = false
max.takeScreenshot = false
max.takeScreenshotForEveryStep = false
max.saveGUITreeToXmlEveryStep =false
max.execSchema = true
max.execSchemaEveryStartup  = true
max.grantAllPermission = true
```

通过adb 命令push 到 android 手机。

```shell
> adb push max.config /sdcard
```

检查文件是否上传成功

```shell
> adb shell

HWJEF:/ $ cd sdcard/

HWJEF:/sdcard $ cat max.config

max.randomPickFromStringList = true
max.takeScreenshot = true
max.takeScreenshotForEveryStep = true
max.saveGUITreeToXmlEveryStep = true
max.execSchema = true
max.execSchemaEveryStartup  = true
max.grantAllPermission = true
```

2. 从文件中随机读取字符串输入

配置`max.config`文件（注：文件名字不可更改）。

```conf
max.randomPickFromStringList = true
max.takeScreenshot = false
max.takeScreenshotForEveryStep = false
max.saveGUITreeToXmlEveryStep =false
max.execSchema = true
max.execSchemaEveryStartup  = true
max.grantAllPermission = true
```

配置 max.strings 文件（注：文件名字不可更改）。
https://github.com/bytedance/Fastbot_Android/blob/main/test/max.strings

```conf
1   香蕉
2   葡萄
3   苹果
```

通过adb 命令push 文件到 android 手机。

```shell
> adb push max.config /sdcard
> adb push max.strings /sdcard
```


## 自定义事件序列

有些App一启动就需要登录，这样遍历工具就停留在登录页面无法继续了。可以通过手动配置Activity 匹配（UI 自动化用例）。

xx App 登录页面：


通过`adb`命令查询当前活动的Activity。

```shell
> adb shell dumpsys activity top | grep ACTIVITY 

ACTIVITY com.xxx/.account_implementation.public_login.PublicLoginPageActivity 451f105 pid=12277
```

配置 `max.xpath.actions` 文件（注：文件名字不可更改）

```json
[
{
    "prob": 1,
    "activity":"com.xxx.account_implementation.public_login.PublicLoginPageActivity",
    "times": 1,
    "actions": [
        {
            "xpath":"//*[@resource-id='com.baidu:id/phone']",
            "action": "CLICK",
            "text": "18911112222",
            "clearText": true,
            "throttle": 2000
        },
        {
            "xpath":"//*[@resource-id='com.baidu:id/pwd']",
            "action": "CLICK",
            "text": "xxxxx",
            "clearText": false,
            "throttle": 2000
        },
        {
            "xpath":"//*[@resource-id='com.baidu:id/nextStepRl']",
            "action": "CLICK",
            "throttle": 2000
        }
    ]
}
]
```

其中xpath元素定位通过`appium inspector` 、`web-editor` 等工具查看。

* 编写事件序列配置（case）：
  - prob：发生概率，"prob"：1,代表发生概率为100%
  - activity：所属场景，详见：三.获取当前页面所属的Activity
  - times：重复次数，默认为1即可
  - actions：具体步骤的执行类型
  - throttle：action间隔事件（ms）

* 支持的元素操作：
action 支持以下类型：必须大写
  - CLICK：点击，想要输入内容在action下补充text，如果有text 则执行文本输入
  - LONG_CLICK：长按
  - BACK：返回
  - SCROLL_TOP_DOWN：从上向下滚动
  - SCROLL_BOTTOM_UP：从下向上滑动
  - SCROLL_LEFT_RIGHT：从左向右滑动
  - SCROLL_RIGHT_LEFT：从右向左滑动

通过adb 命令push 文件到 android 手机。

```shell
> adb push max.xpath.actions /sdcard
```

## 抓取图片和xml结构
保存测试过程中的截图和 xml 结构。

在`max.config`配置文件中设置以属性（文件名不可更改）。

```conf
max.randomPickFromStringList = false
max.takeScreenshot = false
max.takeScreenshotForEveryStep = false
max.saveGUITreeToXmlEveryStep = false
max.execSchema = true
max.execSchemaEveryStartup  = true
max.grantAllPermission = true
```

通过adb 命令push 文件到 android 手机。

```shell
> adb push max.config /sdcard
```

启动fastbot 指定保存的Android手机路径。

```
adb -s UMXDU20813000084 shell CLASSPATH=/sdcard/monkeyq.jar:/sdcard/framework.jar:/sdcard/fastbot-thirdpart.jar exec app_process /system/bin com.android.commands.monkey.Monkey -p com.xxx --agent reuseq --running-minutes 60 --throttle 500 -v -v --output-directory /sdcard/fastbot/
```

- --output-directory  指定手机磁盘路径。

通过adb pull 将要手机磁盘的文件导出到PC电脑。

```shell
> adb pull /sdcard/fastbot ./fastbot/
```

查看截图 和 xml 文件

```shell
> cd fastbot 
> ll
total 9960
-rw-r--r--  1 tech  staff   606K Feb 10 19:32 step-1--g0a11-1644491699842.png
-rw-r--r--  1 tech  staff    17K Feb 10 19:32 step-1--g0a11-1644491699842.xml
-rw-r--r--  1 tech  staff   139K Feb 10 19:32 step-10--g0a23-1644491714512.png
-rw-r--r--  1 tech  staff   7.3K Feb 10 19:32 step-10--g0a23-1644491714512.xml
-rw-r--r--  1 tech  staff   131K Feb 10 19:32 step-11--g0a34-1644491715439.png
-rw-r--r--  1 tech  staff   7.3K Feb 10 19:32 step-11--g0a34-1644491715439.xml
-rw-r--r--  1 tech  staff   164K Feb 10 19:32 step-12--g0a55-1644491716080.png
...
```

## 总结

1. 本文主要参考 fastbot-android 项目文档。

2. 通过对fastbot-android的使用，发现他的可配置东西要高于fastbot-iOS。这主要得益于andriod系统更加开放。

3. 自定义事件序列还是非常有用的，尤其是有些App一打开就需要登录的那种，如果不先登录，后续Monkey 操作就无法进行了。

