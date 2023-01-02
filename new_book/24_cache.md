## 实现简单的缓存

在实际测试过程中，往往需要需要通过cache去临时记录一些数据，从而减少不必要的操作。例如 登录token，很多条用例都会用到登录token，那么就可以借助缓存来暂存登录token，从而减少测试过程中重复登录动作。

实现cache有很多中方式

* 使用 Redis: 使用Redis来做cache是非常普遍的一种手段。
* 使用 文件: 可以简单的利用读写文件实现缓存。

Redis 的优势必然不必多说，利用内存读写速度更快，可以设置自动失效时间。但是，对于自动化测试来说，需要启动一个 Redis 服务显然有点重了，我们考虑第二种方式，通过读写文件，实现一个缓存API。



__功能代码:__

实现Cache的相关API。

```py
# ut_extends/cache.py
import os
import json

FILE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(FILE_DIR, "cache_data.json")


class Cache:
    """
    读写JSON文件实现Cache
    """

    def __init__(self):
        """
        初始化cache文件
        """
        is_exist = os.path.isfile(DATA_PATH)
        if is_exist is False:
            with open(DATA_PATH, "w", encoding="utf-8") as json_file:
                json.dump({}, json_file)

    @staticmethod
    def clear(name: str = None) -> None:
        """
        清理cache
        """
        if name is None:
            with open(DATA_PATH, "w", encoding="utf-8") as json_file:
                print("Clear all cache data")
                json.dump({}, json_file)
        else:
            with open(DATA_PATH, "r+", encoding="utf-8") as json_file:
                save_data = json.load(json_file)
                del save_data[name]
                print(f"Clear cache data: {name}")

            with open(DATA_PATH, "w+", encoding="utf-8") as json_file:
                json.dump(save_data, json_file)

    @staticmethod
    def set(data: dict) -> None:
        """
        设置 cache
        """
        with open(DATA_PATH, "r+", encoding="utf-8") as json_file:
            save_data = json.load(json_file)
            for key, value in data.items():
                data = save_data.get(key, None)
                if data is None:
                    print(f"Set cache data: {key} = {value}")
                else:
                    print(f"update cache data: {key} = {value}")
                save_data[key] = value

        with open(DATA_PATH, "w+", encoding="utf-8") as json_file:
            json.dump(save_data, json_file)

    @staticmethod
    def get(name=None):
        """
        查询cache
        """
        with open(DATA_PATH, "r+", encoding="utf-8") as json_file:
            save_data = json.load(json_file)
            if name is None:
                return save_data

            value = save_data.get(name, None)
            if value is not None:
                print(f"Get cache data: {name} = {value}")
            return value


cache = Cache()

```

__代码说明：__

首先，实现`Cache`类，在`__init__()`初始化方法中判断JSON数据文件是否存在，如果不存在则创建。

接下来，分别实现三个方法

* `clear()`: 清除数据，默认清空整个JSON文件的数据，可以指定 name，即 字典的 key。

* `set()`: 添加数据，以为dict的方式保存。

* `get()`: 获取数据，默认获取整个JSON文件的数据，可以指定 name，即 字典的 key。



__使用实例：__

```py
# test_cache.py
from extends.cache import cache


# 清空缓存
cache.clear()

# 获取指定缓存
token = cache.get("token")
print(f"token: {token}")

# 判断为空写入缓存
if token is None:
    cache.set({"token": "123"})

# 设置存在的数据(相当于更新)
cache.set({"token": "456"})

# value复杂格式设置存在的数据
cache.set({"user": [{"name": "tom", "age": 11}]})


# 获取所有缓存
all_token = cache.get()
print(f"all: {all_token}")

# 清除指定缓存
cache.clear("token")
```

cache 的使用比较简单，参考例子中的注释。


__执行结果__

```shell
> test_cache.py

Clear all cache data
token: None
Set cache data: token = 123
update cache data: token = 456
Set cache data: user = [{'name': 'tom', 'age': 11}]
all: {'token': '456', 'user': [{'name': 'tom', 'age': 11}]}
Clear cache data: token
```
