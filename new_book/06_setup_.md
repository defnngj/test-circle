# 构建python包

前面两节我们分别介绍了开发pytest插件，以及开发unittest扩展，我们开发他们的初衷是为给更多Python开发者使用。那么就需要对他们单独打包。

* 为什么需要对项目分发打包？

我们平时使用pip命令安装第三方模块，这个过程之所以简单，因为第三方模块的的开发者已经将他们的项目进行了打包，并上传到`pypi.org` 官方仓库。

打包，就是将你的项目源代码进一步封装，并且将所有的项目部署工作都事先安排好，这样使用者即装即用，不用操心如何部署的问题。


## setuptools

Setuptools是对Python distutils的一系列增强，它允许开发人员更容易地构建和分发Python包，特别是那些依赖于其他包的包。

> distutils — 构建和安装Python模块。 distutils已弃用，计划在Python 3.12中移除。


以`unittest-extend` 项目为例，目录结构如下：

```shell
unittest-extend/
├── xtest/
│   ├── __init__.py
│   ├── case.py
│   ├── cli.py
│   ├── test.html
├── foo.sh
└── setup.py
```

`setup.py` 文件内容如下：

__基本信息__


```python
from setuptools import setup, find_packages

setup(
    name="xtest",
    version="0.0.1",
    author="bugmaster",
    author_email="fnngj@126.com",
    description="unittest extend",
    long_description="lang description",
    long_description_content_type="text/markdown",
    url="https://github.com/defnngj/unittest-extend",
    packages=find_packages(),
)
````

这里包含了项目的基本信息。

* name: 项目名称。
* version: 项目版本号。
* author: 作者名字。
* author_email: 作者邮箱。
* description: 项目描述，通常一句话。
* long_description: 项目长描述，通常读取描述文件。
* long_description_content_type: 项目长描述的文件格式。
* url: 项目地址
* packages: 安装的包，通过`find_packages`找到当前目录下有哪些包。


__程序分类信息__

`classifiers`参数说明包的分类信息。

```python
from setuptools import setup

setup(
    ...

    classifiers = [
        # 开发的目标用户
        'Intended Audience :: Developers',

        # 属于什么类型
        'Topic :: Software Development :: Testing',

        # 许可证信息
        'License :: OSI Approved :: MIT License',

        # 支持的操作系统
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',

        # 目标 Python 版本
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
```

需要特别注意的是支持python版本，如果我们依赖了`selenium 4.0+ ` 版本，selenium 4.0 仅支持`python 3.7 ~ 3.9` 版本，那么我们的库自然也就支持`python 3.7 ~ 3.9`版本。


__依赖包下载安装__

`install_requires` 用于指定当前库/框架依赖的包。

```py
from setuptools import setup


setup(
    ...

    # 表明当前模块依赖哪些包
    install_requires=[
        'selenium>=4.0.0'
    ],
```

其中，依赖的库需要指定版本。

* `selenium==4.0.0`：等于指定版本。

* `selenium>=4.0.0`：大于等于指定版本。

* `selenium>=3.0.0, != 3.14.1, <=4.0.0`：比较复杂的条件，大于等于某版本，并且小于等于某版本，并且其中排除某版本。


__生成可执行文件__

该配置可以生成命令行工具。

```py
from setuptools import setup


setup(
    ...
    
    # 该文件入口指向 xtest/cli.py 的 `main` 函数
    entry_points={
        'console_scripts': [
            'xt = xtest.cli:main'
        ]
    },

)

```

* `xt`: 即为生成的命令行工具名称。
* `xtest/cli.py` 即为命令行工具的文件。
* `main`: 即为 `cli.py` 文件中的入口方法。

> 如何制作一命令行工具，后面将会介绍。

__指定脚本文件__

`scripts` 指定安装脚本文件。

```py
from setuptools import setup


setup(
    ...
    
    # 指定脚本文件
    scripts=[
        'foo.sh',
        'xtest/test.html'
    ]

)
```

执行安装后，setuptools 会将文件移动到 `/usr/bin` 中（windows 则安装到 `../Python/script/`目录），并添加可执行权限。


现在，你可以试着为你的开源项目创建`setup.py`打包文件了。


### 安装路径


* Windows

`C:\Python38\Lib\site-packages`

* MAC OS

`/Library/Frameworks/Python.framework/Versions/3.8/lib/python3.8/site-packages`



参考：
https://zhuanlan.zhihu.com/p/276461821?utm_oi=948852089393336320

https://zhuanlan.zhihu.com/p/99787649

https://setuptools.pypa.io/en/latest/userguide/quickstart.html
https://setuptools.pypa.io/en/latest/setuptools.html
https://docs.python.org/zh-cn/3/distutils/setupscript.html
https://www.cnblogs.com/maociping/p/6633948.html