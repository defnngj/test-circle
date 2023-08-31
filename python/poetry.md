python包依赖管理和打包工具 - poetry

> 以前，一个开源的项目一定会存在一个  `setup.py` 文件，里面会写上项目的安装信息，然后我们使用 `python setup.py install` 安装项目。你有没有发现越来越多的python项目使用一个叫`pyproject.toml` 文件来代替 `setup.py`。

Poetry是Python中用于依赖管理和打包的工具。它允许声明项目所依赖的库，并将为管理（安装/更新）它们。Poetry提供了一个锁文件来确保可重复安装，并且可以构建你的项目以进行分发。

Poetry可以看作是下一代Python包依赖管理和打包工具。

### 安装

* pip 安装

```shell
> pip install poetry
```

接下来，快速学习Poetry的使用。


### 创建项目

首先，使用poetry创建一个新项目，名命为：poetry-demo：

```shell
> poetry new poetry-demo
```

生成目录结构如下：

```bash
poetry-demo
├── pyproject.toml
├── README.md
├── poetry_demo
│   └── __init__.py
└── tests
    └── __init__.py
```

pyproject.toml 文件是这里最重要的。用于描述项目及其依赖项。内容入如下：

```toml
[tool.poetry]
name = "poetry-demo"
version = "0.1.0"
description = ""
authors = ["fnngj <fnngj@126.com>"]
readme = "README.md"
packages = [{include = "poetry_demo"}]

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

* [tool.poetry] 包含项目的基本信息。
  * name：项目名称。
  * version：项目版本号。
  * description：项目描述，通常一句话。
  * authors：作者名和邮箱。
  * readme：项目描述文件，一般默认为README.md。
  * packages：指定项目的包，poetry_demo目录，一般在该目录下实现项目代码。

* [tool.poetry.dependencies] 用于定义Python版本和第三方库/框架依赖。
  * python = "^3.11"：当前项目依赖Python版本。
  * [build-system] 用于指定构建系统，这部分不需要修改，默认即可。
  * requires：指定“poetry-core”Poetry内核。
  * build-backend：构建后端指定“poetry.core.masonry.api”Poetry的API。


### 安装项目

假如一个项目使用了`pyproject.toml`文件来管理项目，使用如下命令安装项目。

```shell
> > pip install .
Processing d:\github\pytest-hello
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
  Preparing metadata (pyproject.toml) ... done
 ......
```

### 虚拟环境

poetry 支持虚拟环境，可以提供`pipenv`类似的功能，使用如下命令创建虚拟环境。

```shell
> poetry shell
Spawning shell within C:\Users\xxx\AppData\Local\pypoetry\Cache\virtualenvs\pytest-hello-ArB2B-1o-py3.11
Windows PowerShell
Copyright (C) Microsoft Corporation. All rights reserved.

Install the latest PowerShell for new features and improvements! https://aka.ms/PSWindows

Loading personal and system profiles took 885ms.

pytest-hello on  main  🐍 v3.11.4 (pytest-hello-py3.11)
> 
```

现在已经激活了虚拟环境，可以方便的在虚拟化环境中管理项目依赖了。

### 打包

我们通常要将项目进行打包，以便于发布到PyPI上。这样用户就可以通过`pip install xxx` 命令使用我们的包了。

使用如下命令打包项目：

```shell
> poetry build
Building pytest-hello (0.1.0)
  - Building sdist
  - Built pytest_hello-0.1.0.tar.gz
  - Building wheel
  - Built pytest_hello-0.1.0-py3-none-any.whl
```

总之，poetry 提供了非常强大的功能，可以满足我们日常开发的需求。尤其对于Python开源项目开发的用户。

