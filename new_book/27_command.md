# 命令行工具

命令行工具可以有效的提高生产效率，例如，复杂的项目可以使用命令行工具创建脚手架，快速生成项目模板；对于一般性能测试工具，往往也会以命令行的方式提供。

 
实现命令行工具有很多方式：

* sys.args: python 提供的一种简单的方式，argv 用于接收参数变量。
* argparse: Python 内置的用于命令项选项与参数解析的模块。
* 第三方库： 第三方有很多简单好用的CLI库，例如 click、python-fire、typer。


## sys.args 用法

sys 是Python的一个标准库，即`System`的简写，封装了一些系统的信息和接口。argv是 argument variable参数变量的简写形式，一般在命令行调用的时候由系统传递给程序。


__使用例子__


```py
# argv.py
import sys


run_file = sys.argv[0]
print(f"file name -> {run_file}")

args = sys.argv[1:]

for a in args:
    print(f"hello, {a}")

```

__代码说明__

argv 变量其实是一个List列表，argv[0] 一般是被调用的脚本文件名，argv[1:] 表示文件之后传入的数据。

__运行例子__

```shell
> python argv.py tom jerry

file name -> argv.py
hello, tom
hello, jerry
```

## argparse

argparse 模块是 Python 内置的用于命令项选项与参数解析的模块，argparse 模块可以让人轻松编写用户友好的命令行接口。


__使用例子__

```py
# argp.py
import argparse


parser = argparse.ArgumentParser(description='argparse 简单用法')

parser.add_argument('-n', '--name', type=str, default="tom", help="请输入name名字，默认 tom")
parser.add_argument('-c', '--count', type=int, default=1, help="请输入次数，默认1")

args = parser.parse_args()

# 使用参数
name = args.name
count = args.count
for _ in range(count):
    print(f"hello, {name}")

```

__代码说明__

`ArgumentParser()`定义命令行解析器对象。

`add_argument()` 添加命令行参数。

* `-n`，`--name`： 指定参数名。
* type：指定参数类型。
* default: 设置默认值。
* help: 定义帮助信息。

`parse_args()` 从命令行中结构化解析参数。最后，通过 `args.xxx` 使用具体的参数。


__运行例子__

* 查看帮助

```shell
> python args.py --help

usage: argp.py [-h] [-n NAME] [-c COUNT]

argparse 简单用法

optional arguments:
  -h, --help            show this help message and exit
  -n NAME, --name NAME  请输入name名字，默认 tom
  -c COUNT, --count COUNT
                        请输入次数，默认1
```

* 使用命令

```shell
> python argp.py --count 3 --name jack

hello, jack
hello, jack
hello, jack
```


## click

click 是 Python 可组合命令行界面工具包。click借助Python装饰器方式，尽可能少地使用必要的代码，创建漂亮的命令行界面。

__使用例子__


```py
# hello.py
import click


@click.command()
@click.option("-c", "--count", default=1, help="执行次数，默认1。")
@click.option("-n", "--name", prompt="Your name", help="请输入name名字。")
def hello(count, name):
    """简单的程序，问候 count 次 name."""
    for _ in range(count):
        click.echo(f"Hello, {name}!")


if __name__ == '__main__':
    hello()

```

__代码说明__

通过click使用的功能与上一个例子argparse 相同，但是 click 显然更加优化。

`@click.command()` 装饰函数，使之成为命令行接口。

`@click.option()` 装饰函数，为其添加命令行选项等。

* default 设置默认值。
* prompt：当参数为空时，提示输入，类似 input() 的用法。
* help：定义帮助信息。


__运行例子__

* 查看帮助

```shell
> python hello.py --help

Usage: hello.py [OPTIONS]

  简单的程序，问候 count 次 name.

Options:
  -c, --count INTEGER  执行次数，默认1。
  -n, --name TEXT      请输入name名字。
  --help               Show this message and exit.
```

* 使用命令

```shell
> python hello.py -c 3 -n jack
Hello, jack!
Hello, jack!
Hello, jack!

> python hello.py -c 3
Your name: jerry  <-- 需要手动输入name
Hello, jerry!
Hello, jerry!
Hello, jerry!
```

