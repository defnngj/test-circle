# 命令行工具实战

通过前面的学习，我们对命令行工具有初步的了解。命令行工具应用比较广泛，本节，我们将通过一些例子演示用法。


### 实现脚手架

做过Web自动化测试项目的同学应该知道，创建自动化测试项目会有比较固定的目录结构，例如。

```tree
├───reports  // 测试报告
├───test_data  // 测试数据
├───test_case  // 测试用例
│   ├───test_sample.py
└───run.py  // 运行文件
```

你一定见过类似的自动化测试项目目录结构。我们可以实现脚手架工具来自动生成项目。


__使用例子__

利用click库实现创建自动化测试项目的脚手架工具。

```py
import os
import click


@click.command()
@click.option("-P", "--project", help="创建项目脚手架。")
def main(project):
    """简单的命令行工具."""
    if project:
        create_scaffold(project)
        return 0


def create_scaffold(project_name: str) -> None:
    """
    创建指定项目名称的脚手架。
    :param project_name:  项目名称
    :return:
    """

    if os.path.isdir(project_name):
        print(f"Folder {project_name} exists, please specify a new folder name.")
        return

    print(f"Start to create new test project: {project_name}")
    print(f"CWD: {os.getcwd()}\n")

    def create_folder(path: str):
        """
        创建目录
        :param path: 路径
        :return:
        """
        os.makedirs(path)
        print(f"created folder: {path}")

    def create_file(path: str, file_content: str = ""):
        """
        创建文件
        :param path: 路径
        :param file_content: 文件内容
        :return:
        """
        with open(path, 'w', encoding="utf-8") as py_file:
            py_file.write(file_content)
        msg = f"created file: {path}"
        print(msg)

    test_sample = '''import unittest


class MyTest(unittest.TestCase):

    def test_case(self):
        self.assertEqual(2+2, 4)


if __name__ == '__main__':
    unittest.main()

'''

    run = '''import unittest

suit = unittest.defaultTestLoader.discover("test_dir", "test_*.py")

runner = unittest.TextTestRunner()
runner.run(suit)

'''
    create_folder(project_name)
    create_folder(os.path.join(project_name, "test_dir"))
    create_folder(os.path.join(project_name, "reports"))
    create_folder(os.path.join(project_name, "test_data"))
    create_file(os.path.join(project_name, "test_dir", "__init__.py"))
    create_file(os.path.join(project_name, "test_dir", "test_sample.py"), test_sample)
    create_file(os.path.join(project_name, "run.py"), run)


if __name__ == '__main__':
    main()

```


__代码说明__

`-P/--project` 定义创建项目的参数。

`create_scaffold()` 函数用于创建脚手架。`create_folder()` 用于创建目录；`create_file()` 用于创建文件。 



__运行例子__

* 查看帮助

```shell
> python cli.py --help

Usage: cli.py [OPTIONS]

  简单的命令行工具.

Options:
  -P, --project TEXT  创建项目脚手架。
  --help              Show this message and exit.
```

* 使用命令

```shell
> python cli.py --project mypro

Start to create new test project: mypro
CWD: D:\github\code\extends\command

created folder: mypro
created folder: mypro\test_dir
created folder: mypro\reports
created folder: mypro\test_data
created file: mypro\test_dir\__init__.py
created file: mypro\test_dir\test_sample.py
created file: mypro\run.py
```
然后，你会在当目录下得到一个名为 mypro 的项目目录，下面将会生成列表中的目录和文件。


### 实现性能工具

我们应该见过不少性能测试工具都是以命令行专方式提供的，或者提供的有命令行模式，例如 ab(Apache HTTP server benchmarking tool)、 locust 等。


__使用例子__

这个例子稍微有些复杂，会涉及到额外的几个库：

* gevent: gevent 是一个基于协程的 Python 网络库，它使用 greenlet 在 libev 或 libuv 事件循环之上提供高级同步API。我们知道性能工具核心就是模拟并发请求，通过 gevent 模拟并发，在同等配置下可以有更好的性能。
* requests: 一个HTTP(s)客户端库，用来发送HTTP请求。性能测试模拟用户并发，本质上是向服务端发送请求。
* tqdm：用于显示进度条的一个库，性能测试运行过程通过tqdm 可以直观的看到运行进度。
* numpy：Python的一种开源的数值计算扩展，用他来统计测试结果非常方便。

```py
# kb.py
import gevent
from gevent import monkey
monkey.patch_all()
import time
import click
import requests
from numpy import mean
from tqdm import tqdm


class Statistical:
    """统计类"""
    pass_number = 0
    fail_number = 0
    run_time_list = []


def running(url, request):
    """运行请求调用"""
    for _ in tqdm(range(request)):
        start_time = time.time()
        r = requests.get(url)
        if r.status_code == 200:
            Statistical.pass_number = Statistical.pass_number + 1
        else:
            Statistical.fail_number = Statistical.fail_number + 1

        end_time = time.time()
        run_time = round(end_time - start_time, 4)
        Statistical.run_time_list.append(run_time)


@click.command()
@click.argument('url')
@click.option('-u', '--user', default=1, help='运行用户的数量，默认 1', type=int)
@click.option('-q', '--request', default=1, help='单个用户请求数，默认 1', type=int)
def main(url, user, request):
    print(f"请求URL: {url}")
    print(f"用户数：{user}，循环次数: {request}")
    print("============== Running ===================")

    jobs = [gevent.spawn(running, url, request) for _url in range(user)]
    gevent.wait(jobs)

    print("\n============== Results ===================")
    print(f"最大:       {str(max(Statistical.run_time_list))} s")
    print(f"最小:       {str(min(Statistical.run_time_list))} s")
    print(f"平均:       {str(round(mean(Statistical.run_time_list), 4))} s")
    print(f"请求成功: {Statistical.pass_number}")
    print(f"请求失败: {Statistical.fail_number}")
    print("================== end ====================")


if __name__ == "__main__":
    main()
```

__代码说明__

首先， gevent 导入顺序必须放到最前面，`monkey.patch_all()` 用于解决协程堵塞问题。

通过 click 实现命令行工具，接收三个参数，url 默认第一，且必传； user 设置请求用户数，request 设置每个用户请求次数。

`gevent.spawn()` 用于创建一个协程并且运行，根据user的数量创建相应数量的协程。

`running()` 函数通过 requests库根据request数量发送请求，判断返回HTTP状态码是否为200。

最后，针对请求的次数、时间进行统计。

__使用说明__

* 查看帮助

```shell
>  python kb.py --help
Usage: kb.py [OPTIONS] URL

Options:
  -u, --user INTEGER     运行用户的数量，默认 1
  -q, --request INTEGER  单个用户请求数，默认 1
  --help                 Show this message and exit.
```

* 使用命令

```shell
> python kb.py https://www.baidu.com -u 2 -q 10

请求URL: https://www.baidu.com
用户数：2，循环次数: 10
============== Running ===================
100%|████████████████████████████████████████████████████████████████████████| 10/10 [00:01<00:00,  8.37it/s]
100%|████████████████████████████████████████████████████████████████████████| 10/10 [00:01<00:00,  8.01it/s]

============== Results ===================
最大:       0.1613 s
最小:       0.1003 s
平均:       0.1216 s
请求成功: 20
请求失败: 0
================== end ====================
```


### 生成命令行工具

直到目前为止，我们虽然可以利用 click 实现类似命令行工具，但我们直到真正的命令行工具是不用 "python xxx.py" 的，而是直接在任意位置使用 `xxx` 即可。

我们需要将脚本与 setuptools 捆绑到一起，只需要创建 setup.py 文件即可，在本书的第一章就介绍了 setup.py 文件的创建。

```tree
├───kb.py     # 命令行脚本
└───setup.py  # 安装脚本
```

实现 setup.py 文件。

```py
# setup.py
from setuptools import setup

setup(
    name='kb',
    description="kb - 简单性能测试工具",
    version='0.1.0',
    py_modules=['kb'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'kb = kb:main',
        ],
    },
)
```

`entry_points` 指定入口，kb 即命令工具的名称，kb:main 对应 kb.py 文件中的 main() 函数。


__执行安装__

执行 setup.py 文件安装kb命令行工具。

```shell
> python setup.py install
```

通过 pip 查看安装信息

```shell
> pip show kb
Name: kb
Version: 0.1.0
Summary: kb - 简单性能测试工具
Home-page: UNKNOWN
Author: UNKNOWN
Author-email: UNKNOWN
License: UNKNOWN
Location: c:\python38\lib\site-packages\kb-0.1.0-py3.8.egg
Requires: Click
Required-by:
```

为了使 setup.py 足够简洁，一些参数没有定义，例如 Home-page、author、 author-email、License， 所以默认为 UNKNOWN。

__使用命令行工具__

确认安装成功后，我们可以在任何位置使用kb命令了。

```
> kb --help
Usage: kb [OPTIONS] URL

Options:
  -u, --user INTEGER     运行用户的数量，默认 1
  -q, --request INTEGER  单个用户请求数，默认 1
  --help                 Show this message and exit.
```

至此，我们设计了出了一个命令行性能测试工具，值得庆祝一下！
