## 实现日志

无论是写框架代码还是业务代码，日志能给定位问题带来极大的帮助。

记录日志最简单的方法就是在你想要记录的地方使用`print()`方法，我相信无论是新手还是老鸟都经常这么干。在简单的代码中或者小型项目中这么干一点问题都没有。但是在一些稍大一点的项目，有时候定位一个问题，需要查看历史日志定位问题，用`print()`语句就不合时宜了。

`print()`语句打印出来的日志没有时间，不知道日志记录的位置，也没有可读的日志格式， 还不能把日志输出到指定文件，除非这些你都全部自己重复造一遍轮子。

在Python中使用日志有两种方式：

* Python自带 logging 模块。
* Python第三方日志库。

在此，我以个人的使用经验介绍Python日志相关模块/库，以及用法。

### logging 模块


__使用例子__

先来熟悉一下python logging模块的基本用法。

```python
# sys_logging.py
import logging

logging.basicConfig(level=logging.DEBUG)

logging.debug("this is debug")
logging.info("this is info")
logging.warning("this is warning")
logging.error("this is error")
logging.critical("this is critical")
```

__使用说明__

* basicConfig() 设置logging基本配置，level指定日志打印级别。
* logging分为5个等级：
  * debug：调试
  * info： 信息
  * warning：警告
  * error：错误
  * critical：严重

__运行结果__

```shell
DEBUG:root:this is debug
INFO:root:this is info
WARNING:root:this is warning
ERROR:root:this is error
CRITICAL:root:this is critical
```

上面介绍的日志记录，其实是通过一个叫做日志记录器（Logger）的实例对象创建的，每个记录器都有一个名称，直接使用logging来记录日志时，系统会默认创建名为 root 的记录器，这个记录器是根记录器。

__功能代码__

接下来，实现自定义日志类 MyLog。

```python
# sys_logging.py
import logging
from logging import StreamHandler
from logging import FileHandler


class MyLog:

    def __init__(self, name=__name__, level=logging.DEBUG, logfile="log.log"):
        """
        基本配置
        :param name: 调用日志模块名
        :param level: 日志级别
        :param logfile: 日志文件
        """

        # 自定义日志格式
        formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 标准流处理
        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # 文件处理器
        file_handler = FileHandler(filename=logfile)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """ debug log """
        self.logger.debug(message)

    def info(self, message: str) -> None:
        """ info log """
        self.logger.info(message)

    def warning(self, message: str) -> None:
        """ warning log """
        self.logger.warning(message)

    def error(self, message: str) -> None:
        """ error log """
        self.logger.error(message)

    def critical(self, message: str) -> None:
        """ critical log """
        self.logger.critical(message)
```

__代码说明__

* Formatter() 类实现自定义日志格式。然后，通过 setFormatter() 方法设置使自定义格式生效。
* getLogger() 类即日志记录器，记录器名称可以是任意名称，不过最佳实践是直接用模块的名称（\_\_name\_\_）当作记录器的名字。
* StreamHandler() 类定义输出流，可以理解为控制台输出。
* FileHandler() 类定义文件输出，同样也可以将日志保存到日志文件中，这一功能在服务器上执行尤为重要，通过日志文件定位问题是线上排查问题的重要手段。
* 最终通过addHandler() 方法添加Handler，使配置生效。


__使用例子__

调用 sys_logging 文件封装的MyLog()类。

```py
# test_logging.py
from extends.sys_logging import MyLog

log = MyLog(__name__)

log.debug("this is debug")
log.info("this is info")
log.warning("this is warning")
log.error("this is error")
log.critical("this is critical")
```

__运行结果__

* 终端输出

```shell
> python test_logging.py

[2022-12-25 23:32:08,388] __main__ - DEBUG - this is debug
[2022-12-25 23:32:08,389] __main__ - INFO - this is info
[2022-12-25 23:32:08,389] __main__ - WARNING - this is warning
[2022-12-25 23:32:08,389] __main__ - ERROR - this is error
[2022-12-25 23:32:08,390] __main__ - CRITICAL - this is critical
```

* log.log 文件输出

```log
# log.log
[2022-12-25 23:32:08,388] __main__ - DEBUG - this is debug
[2022-12-25 23:32:08,389] __main__ - INFO - this is info
[2022-12-25 23:32:08,389] __main__ - WARNING - this is warning
[2022-12-25 23:32:08,389] __main__ - ERROR - this is error
[2022-12-25 23:32:08,390] __main__ - CRITICAL - this is critical
```

### colorama

colorama是一个Python专门用来在控制台、命令行输出彩色文字的模块，可以跨平台使用。

* pip 安装 colorama

```
> pip install colorama
```

__使用例子__

利用 coclorama 为不同级别的日志设置不同的颜色。

```py
# color_logging.py
import logging
from logging import StreamHandler
from logging import FileHandler
from colorama import Fore, Style


class MyLog:

    def __init__(self, name=__name__, level=logging.DEBUG, logfile="log.log"):
        """
        日志基本配置
        :param name: 模块名字
        :param level: 日志级别
        :param logfile: 日志文件
        """
        # 自定义日志格式
        formatter = logging.Formatter('[%(asctime)s] %(name)s - %(levelname)s - %(message)s')

        # 自定义日志格式
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # 标准流处理
        stream_handler = StreamHandler()
        stream_handler.setFormatter(formatter)
        self.logger.addHandler(stream_handler)

        # 文件处理器
        file_handler = FileHandler(filename=logfile)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def debug(self, message: str) -> None:
        """ debug log """
        self.logger.debug(Fore.CYAN + str(message) + Style.RESET_ALL)

    def info(self, message: str) -> None:
        """ info log """
        self.logger.info(Fore.GREEN + str(message) + Style.RESET_ALL)

    def warning(self, message: str) -> None:
        """ warning log """
        self.logger.warning(Fore.YELLOW + str(message) + Style.RESET_ALL)

    def error(self, message: str) -> None:
        """ error log """
        self.logger.error(Fore.RED + str(message) + Style.RESET_ALL)

    def critical(self, message: str) -> None:
        """ critical log """
        self.logger.critical(Fore.BLUE + str(message) + Style.RESET_ALL)

```

__代码说明__

相比较 sys_logging.py 文件的封装，主要变化在debug()/info()/warning()/error()/critical()几个方法；Fore 分别为不同级别的日志指定不同的颜色； `Style.RESET_ALL`表示全部重设。


__使用例子__

调用 color_logging 文件封装的MyLog()类。

```py
# test_logging.py
from extends.color_logging import MyLog

log = MyLog(__name__)

log.debug("this is debug")
log.info("this is info")
log.warning("this is warning")
log.error("this is error")
log.critical("this is critical")
```

__运行结果__

* 终端输出

```shell
> python test_logging.py

[2022-12-25 23:32:08,388] __main__ - DEBUG - this is debug
[2022-12-25 23:32:08,389] __main__ - INFO - this is info
[2022-12-25 23:32:08,389] __main__ - WARNING - this is warning
[2022-12-25 23:32:08,389] __main__ - ERROR - this is error
[2022-12-25 23:32:08,390] __main__ - CRITICAL - this is critical
```

因为本书为黑白打印，你无法看到彩色效果，可以在本地运行上面的代码进行验证。


### Loguru


Loguru是一个库，旨在为Python带来愉快的日志记录。

* pip 安装 loguru

```
> pip install loguru
```


__使用例子__

为方便起见，loguru是预先配置的，并首先输出到 stderr。如果没有特殊的要求，loguru可以达到开箱即用。

```py
# test_loguru.py
from loguru import logger

logger.debug("this is debug!")
logger.info("this is info!")
logger.warning("this is warning!")
logger.error("this is error!")
logger.success("this is success!")

```

__运行结果__

* 终端输出

```shell
> python test_loguru.py

2023-01-02 14:33:25.925 | DEBUG    | __main__:<module>:4 - this is debug!
2023-01-02 14:33:25.925 | INFO     | __main__:<module>:5 - this is info!
2023-01-02 14:33:25.925 | WARNING  | __main__:<module>:6 - this is warning!
2023-01-02 14:33:25.925 | ERROR    | __main__:<module>:7 - this is error!
2023-01-02 14:33:25.925 | SUCCESS  | __main__:<module>:8 - this is success!
```

__更多用法__

loguru 同样支持日志格式，级别，和 日志文件等配置。

```py
# test_loguru.py
import sys
import time
from loguru import logger

# 自定义log格式
log_format = "<green>{time:YYYY-MM-DD HH:mm:ss}</> {file} <level>| {level} | {message}</level>"

# stderr 配置
logger.remove()
logger.add(sys.stderr, format=log_format, level="DEBUG")

# log 文件配置
logger.add(f"file_{time.time()}.log", rotation="12:00", format=log_format)


logger.debug("this is debug!")
logger.info("this is info!")
logger.warning("this is warning!")
logger.error("this is error!")
logger.success("this is success!")

```

__运行结果__

* 终端输出

```shell
> python test_loguru.py

2023-01-02 14:54:49 test_loguru.py | DEBUG | this is debug!
2023-01-02 14:54:49 test_loguru.py | INFO | this is info!
2023-01-02 14:54:49 test_loguru.py | WARNING | this is warning!
2023-01-02 14:54:49 test_loguru.py | ERROR | this is error!
2023-01-02 14:54:49 test_loguru.py | SUCCESS | this is success!
```

* 日志文件输出（file_1672642489.2261276.log）

```shell
2023-01-02 14:54:49 test_loguru.py | DEBUG | this is debug!
2023-01-02 14:54:49 test_loguru.py | INFO | this is info!
2023-01-02 14:54:49 test_loguru.py | WARNING | this is warning!
2023-01-02 14:54:49 test_loguru.py | ERROR | this is error!
2023-01-02 14:54:49 test_loguru.py | SUCCESS | this is success!
```
