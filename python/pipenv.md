
# python多版本与虚拟环境

这篇纯python技术文章，我自己平时也会用到，在此记录一下。

## 为什么会用到多个Python版本？

用macOS和Ubutntu的同学都知道系统默认安装的`Python2.7.x`，然后，我们平时python开发用的python3，所以，需要额外安装一个`Python3.x`的版本。

之前，我想是使用robotframework-ride但它只支持python3.7，于是，我安装python3.7。（注：现在已经支持3.8了）

前几天，我想学习一下tinygrad，他支持python3.8，于是，我又装了3.8。

## python多版本管理

1. 使用Where查找安装的`python`、`python3` 路径。

* macOS终端：

```shell
❯ where python  
/usr/bin/python    # 2.7.16

❯ where python3
/Library/Frameworks/Python.framework/Versions/3.7/bin/python3  # 3.7.9
/usr/local/bin/python3  # 3.7.9
/usr/bin/python3  # 3.7.3
```

* windows命令提示符

```shell
❯ where python
C:\Python37\python.exe
C:\Python38\python.exe
C:\Users\fnngj\AppData\Local\Microsoft\WindowsApps\python.exe
```

2. 为不同的python 改名字。
比如， `C:\Python38\python.exe` 文件拷贝改名为 `C:\Python38\py8.exe`，那我就可以愉快的使用py8这个命令了。

```shell
❯ py8
Python 3.8.6 (tags/v3.8.6:db45529, Sep 23 2020, 15:52:53) [MSC v.1927 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

3. 为不同的python 安装库。

每个python版本下面都有 pip，我们在使用pip的安装库的时候，经常不知道他安装在哪个python下面了。

```shell
❯ py8 -m pip install selenium
❯ py8 -m pip show selenium
...
Location: c:\python38\lib\site-packages
...
```

带上 `python -m`的前缀，这样永远不会装错。


## 为什么会用虚拟环境？

作为一个使用python开发过大型项目的同学，一定会碰到python库的版本依赖。

例如 直接依赖：

* A项目：使用 django 2.2
* B项目：使用 django 3.1

还有复杂的间接依赖：

* A项目：使用A框架 ——> 依赖 requests 1.10
* B项目：使用B库 ——> 依赖 requests 2.x

而你又需要同时开发A、B两个项目，总不能在运行不同的项目的时候，就把不同项目的依赖库装一遍吧！

## 虚拟环境管理

python的虚拟环境管理工具挺多的，virtualenv、virtualenvwrapper、pipenv，pyenv。其实明白了原理这些工具都不复杂，这里以pipenv为例。

1. 安装pipenv

```shell
❯ pip install pipenv
```

2. 创建虚拟环境

进入到项目目录，创建虚拟环境。

```shell
❯ cd mypro  # 进入项目目录

❯ pipenv --python py8  # 指定基于哪个python版本创建虚拟环境。
Creating a virtualenv for this project...
Pipfile: D:\github\mypro\Pipfile
Using C:/Python38/py8.exe (3.8.6) to create virtualenv...
...
Successfully created virtual environment!
Virtualenv location: C:\Users\fnngj\.virtualenvs\mypro-D2Xyk8c9
```

3. 安装依赖

这一步从Pipfile.loc中安装依赖。

```shell
❯ pipenv install
Installing dependencies from Pipfile.lock (db4242)...
  ================================ 0/0 - 00:00:00
To activate this project's virtualenv, run pipenv shell.
Alternatively, run a command inside the virtualenv with pipenv run.
```

4. 进入虚拟环境

```shell
❯ pipenv shell
Launching subshell in virtual environment...
```

5.可以在虚拟环境里面安装你想要的应用了。
```shell
v3.8.6 ((mypro)) ❯ pip install xxx
```

6.退出虚拟环境

```shell
v3.8.6 ((mypro)) ❯ exit;
```

7.删除虚拟环境
```shell
❯ pipenv --rm
```

注：其实这两个管理在pycharm集成的就有，可是上来就完全依赖pycharm开发python的同学很难搞清楚。那么，本文也有助于你更好的使用 pycharm。