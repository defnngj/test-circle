## 自动化之cache的使用


在自动化测试过程中，往往需要通过cache去记录一些数据，从而减少重复的操作。例如，登录token，假设 100 条用例都需要执行 `login()` 方法，获取登录token。在 __登录账号相同__ 的情况下，当第一条用例执行了登录，之后的用例就可以直接使用第一条用例获取的token，没必要重复执行登录操作。

Python 实现 cache 会有以下几种方式：

* lru_cache
* 磁盘文件读写模拟cache
* redis

### lru_cache

LRU全称是Least Recently Used，即 __最近最久未使用__ 的意思。LRU算法的设计原则是：如果一个数据在最近一段时间没有被访问到，那么在将来它被访问的可能性也很小。


python 提供了 lru_cache 装饰器，用法非常简单，只需要装饰需要缓存的方法即可。

* 使用例子

```py
# test_cache_01.py
import hashlib
from time import sleep, time
from functools import lru_cache


@lru_cache(None)
def login(username, password):
    """模拟登录生成token"""
    sleep(5)
    src = f'{username}.{password}'
    m = hashlib.md5()
    m.update(src.encode("utf-8"))
    token = m.hexdigest()
    return token


def test_case1():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case2():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case3():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")

```

__代码说明__

通过`login()` 模拟用户登录，根据传入的 username/password 生成md5 字符串，假设为登录token串。然后，通过`lru_cache()` 对其进行装饰。

创建三条用例，分别调用 `login()` 方法，而参数一样。

* 运行结果

```shell
> pytest -vs test_cache_01.py

……

collected 3 items

test_cache_01.py::test_case1 token: fccd7ab1a9d96d2fae0f7c37ce4abe01, run time:5.009549856185913
PASSED
test_cache_01.py::test_case2 token: fccd7ab1a9d96d2fae0f7c37ce4abe01, run time:0.0
PASSED
test_cache_01.py::test_case3 token: fccd7ab1a9d96d2fae0f7c37ce4abe01, run time:0.0
PASSED

========================================== 3 passed in 5.47s ======================
```

我们特意在 `login()` 方法中加入了sleep() 模拟方法耗时，从结果可以看到，只有第一条用例耗时 5s ，后面两条用例直接返回了结果。

> python 3.9 提供了cache， 返回与 lru_cache（maxsize=None）相同的值，围绕函数参数的字典查找创建精简包装器。 用法进一步简化。

__总结：__

python 提供的 lru_cache/cache 用法非常简单，合理的使用 可以有效的减少不必要的重复操作，有效降低测试用例的运行时间。当然了唯一的缺点就是无法做到数据的持久化，他是基于内存是实现 cache 的方式，一旦程序运行结束，内存就释放掉了。


### 磁盘文件读写模拟cache

这种方式本质上是通过文件的读写将数据保存到磁盘上，实现起来并不复杂，seldom框架提供了这种方案，我直接拿来用了。

* 安装 seldom

```
> pip install seldom
```

* 使用例子

```py
# test_cache_02.py
import hashlib
from time import sleep, time
from seldom.utils import cache


def login(username, password):
    """模拟登录生成token"""
    token = cache.get(username)
    # 如果有token 直接返回
    if token is not None:
        return token

    sleep(5)
    src = f'{username}.{password}'
    m = hashlib.md5()
    m.update(src.encode("utf-8"))
    token = m.hexdigest()
    # 写入 token
    cache.set({username: token})

    return token


def test_case1():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case2():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case3():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")

```

__代码说明__

在 `login()` 方法中 获取 token 进行判断，如果有直接返回，如果没有生成token，然后把token 写入 cache。

* 运行结果

```shell
> pytest -vs test_cache_02.py

test_cache_02.py::test_case1 2023-03-30 23:53:06 cache.py | INFO | Set cache data: admin = fccd7ab1a9d96d2fae0f7c37ce4abe01
token: fccd7ab1a9d96d2fae0f7c37ce4abe01, run time:5.003232717514038
PASSED
test_cache_02.py::test_case2 2023-03-30 23:53:06 cache.py | INFO | Get cache data: admin = fccd7ab1a9d96d2fae0f7c37ce4abe01
token: fccd7ab1a9d96d2fae0f7c37ce4abe01, run time:0.0009968280792236328
PASSED
test_cache_02.py::test_case3 2023-03-30 23:53:06 cache.py | INFO | Get cache data: admin = fccd7ab1a9d96d2fae0f7c37ce4abe01
token: fccd7ab1a9d96d2fae0f7c37ce4abe01, run time:0.0009968280792236328
PASSED

========================================= 3 passed in 6.95s ====================
```

通过结果可以看到，只有第一条用例耗时5s， 后面个两条用例直接获取的token返回。

__总结：__

通过磁盘文件读写模式cache，可以更好的控制cache的有效时间。比如，再次执行三条用例，就不再消耗登录时间了，当然，这都需要你手动控制 什么时候读、什么时候写、什么时候清除。

最近，发现这种方案有个致命问题，就是多线程运行测试的时候，因为并发读写一个文件不同的数据，会导致文件读写错误。加文件读写锁也不能很好的解决，为每个数据都单独创建一个文件可以避免这个文件，但生成一堆文件的做法着实不算优雅。


### redis

Redis全称为Remote Dictionary Server（远程数据服务），是一款开源的基于内存的键值对存储系统，其主要被用作高性能缓存服务器使用，当然也可以作为消息中间件和Session共享等。

无需过多介绍，他广泛应用于各种系统，有效的减少数据库访问，提高系统数据访问速度。

* 安装 redis

https://github.com/redis/redis


* 安装 redis-py

```
> pip install redis
```

* 使用例子

```py
import hashlib
from time import sleep, time
import redis


def login(username, password):
    """模拟登录生成token"""
    r = redis.Redis(host='localhost', port=6379, db=0)
    token = r.get(username)
    # 如果有token 直接返回
    if token is not None:
        return token

    sleep(5)
    src = f'{username}.{password}'
    m = hashlib.md5()
    m.update(src.encode("utf-8"))
    token = m.hexdigest()
    # 写入 token
    r.set(username, token)

    return token


def test_case1():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case2():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")


def test_case3():
    start = time()
    token = login("admin", "abc123")
    end = time()
    print(f"token: {token}, run time:{ end - start}")

```

__代码说明__

在 login() 中实现redis 的连接，显然不是好方法，应该有 测试执行入口方法来完成，为了简化例子，就这么实现了。测试用例与前两个例子保持一直。


__运行结果__

```
> pytest -vs test_cache_03.py

test_cache_03.py::test_case1 token: fccd7ab1a9d96d2fae0f7c37ce4abe01, run time:7.044048070907593
PASSED
test_cache_03.py::test_case2 token: b'fccd7ab1a9d96d2fae0f7c37ce4abe01', run time:2.0274996757507324
PASSED
test_cache_03.py::test_case3 token: b'fccd7ab1a9d96d2fae0f7c37ce4abe01', run time:2.0378215312957764
PASSED

==================================== 3 passed in 11.59s ===========================
```

从运行结果可以看到，redis 的连接还是比较耗时的，平均多消耗2s。


__总结：__

通过redis缓存数据无疑是最强大的，比如，token 的有效期是5小时，你就可以在set 时设置5小时，不用再手动清理缓存了。

当然，缺点是需要单独启动一个redis服务，对于自动化测试来说，有点重了，每个要运行的环境，都需要启动一个redis服务，或者，你们也可以内部部署一个redis服务，不同的环境可以通过地址连接。

最后，不管哪种cache 方案，都有优、缺点，关键是找到合适的方式。

