## 炫酷的终端库 Rich

> 作为一个终端爱好者，我几乎不用 `vscode`, `pycharm` 去运行程序，除非需要debug调试的时候，我会特别关注各种好看的终端工具。今天推荐宝藏终端库 Rich。

Rich 是一个 Python 库，可以为您在终端中提供富文本和精美格式。

Rich 的 API 让在终端输出颜色和样式变得很简单。此外，Rich 还可以绘制漂亮的表格、进度条、markdown、语法高亮的源代码以及栈回溯信息（tracebacks）等——开箱即用。

## 安装：

* pip 安装：

```
python -m pip install rich
```

## 基本使用

* rich 打印功能

```python
from rich import print

print("Hello, [bold magenta]World[/bold magenta]!", ":vampire:")
```

* 日志工具

```python
import logging
from rich.logging import RichHandler

FORMAT = "%(message)s"
logging.basicConfig(
    level="NOTSET", format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
)

log = logging.getLogger("rich")
log.info("Hello, World!")

```


* 多进度条

```python
from time import sleep
from rich.live import Live
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from rich.table import Table


# 进度条样式
job_progress = Progress(
    "{task.description}",
    SpinnerColumn(),
    BarColumn(),
    TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
)
# 进度条数量
for _ in range(3):
    job_progress.add_task("[green]User")


total = sum(task.total for task in job_progress.tasks)
overall_progress = Progress()
overall_task = overall_progress.add_task("All Jobs", total=int(total))


# 进度表
progress_table = Table.grid()
progress_table.add_row(
    Panel.fit(
        overall_progress, title="Overall Users", border_style="green", padding=(2, 2)
    ),
    Panel.fit(job_progress, title="[b]Jobs", border_style="red", padding=(1, 2)),
)

# 运行
with Live(progress_table, refresh_per_second=10):
    while not overall_progress.finished:
        sleep(0.1)
        for job in job_progress.tasks:
            if not job.finished:
                job_progress.advance(job.id)
        completed = sum(task.completed for task in job_progress.tasks)
        overall_progress.update(overall_task, completed=completed)

```

* 表格

```python
from rich.console import Console
from rich.table import Column, Table

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Date", style="dim", width=12)
table.add_column("Title")
table.add_column("Production Budget", justify="right")
table.add_column("Box Office", justify="right")
table.add_row(
    "Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$275,000,000", "$375,126,118"
)
table.add_row(
    "May 25, 2018",
    "[red]Solo[/red]: A Star Wars Story",
    "$275,000,000",
    "$393,151,347",
)
table.add_row(
    "Dec 15, 2017",
    "Star Wars Ep. VIII: The Last Jedi",
    "$262,000,000",
    "[bold]$1,332,539,889[/bold]",
)

console.print(table)
```


## 性能测试工具

这个好玩的工具能干点啥呢？我之前分享过如何使用python开发一个命令行性能测试工具。许多信息是需要在终端输出的。那么刚好可以通过`Rich`美化一下。

https://github.com/SeldomQA/kb

具体代码我就不介绍，之前的文章做过了详细开发介绍。

> 注： 这只是一个玩具项目，当然不能和JMeter，甚至是别的命令行性能工具比较。

* 最终使用效果

