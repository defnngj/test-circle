## 生成随机数

测试数据是测试用例的重要部分，有时不能把测试数据写死在测试用例中，例如，注册新用户，每次注册都要使用一个未注册过的账号；预定酒店查询，每天去查询所使用的日期都不同；类似的这些功能就需要用到随机生成数据的方法。


生成随机数据的有两种方式：

* 使用现成的库：例如 faker 就是非常强大的生成随机数据的工具，常见的数据都可以用他来生成。

* 自己封装：因为每个公司的业务都不尽相同，所以用到的数据格式也不完全一样，针对自己的业务去做随机数据的封装更加精准。


## 测试工具介绍


### testdata 

testdata 是一个非常简单的库，用于生成随机测试数据。他只提供了一堆方便的函数，旨在使测试代码更容易。

* pip 安装 testdata

```
> pip install testdata
```


__使用例子__

通过例子了解testdata提供的一些方法。

```py
# testdata_sample.py
from testdata import *

# 生成ascii码
asc = get_ascii(str_size=0)
print(asc)

# 生成md5
md5 = get_md5()
print(md5)

# 生成hash
ha = get_hash(str_size=32)
print(ha)

# 随机生成布尔
b = get_bool()
print(b)

# 生成float浮点数
f = get_float(min_size=None, max_size=None)
print(f)

# 生成int整型数
i = get_int(min_size=1, max_size=sys.maxsize)
print(i)

# 生成name
n = get_name(name_count=2, as_str=True)
print(n)

# 生成email
e = get_email()
print(e)

# 生成字符串
s = get_str(str_size=0, chars=None)
print(s)

# 生成url
u = get_url()
print(u)

# 生成单词
w = get_words(word_count=0, as_str=True)
print(w)

# 生成过去时间
pd = get_past_datetime()
print(pd)

# 生成未来时间
fd = get_future_datetime()
print(fd)
```

__使用例子__

testdata所提供的方法非常简单，甚至不需要做过多解释。除了上面提供的一些和测试数据相关的方法，还提供了一些其他方法，例如 运行命令的方法，创建线程或创建文件。

虽然，testdata他没什么名气，但他足够简单，我们在设计生成随机数的时候可以参考他的代码。

__运行结果__

```
> python testdata_sample.py
生成ascii码: G4Fr
生成md5: db5007be61c19cec0019871c964a064f
生成hash: 6s7PoHWhGeP77oVrRgTvLQkAK9HVl0YF
随机生成布尔: True
生成float浮点数: 8.81940582740625e+307
生成int整型数: 2528892783050688712
生成name: Kelley Bright
生成email: jenny@yahoo.ca
生成字符串: Lk濙)ȳȗ
生成url: http://JXkgpKrn.com
生成单词: Phasellus quis ante hendrerit est последний laoreet tortor ligula. imperdiet orci. об дом vitae aliquam pretium
生成过去时间: 2021-09-23 13:29:48.668330
生成未来时间: 2048-10-08 04:17:41.669319
```

### faker

Faker是一个Python包，可以为你伪造数据。无论是需要引导数据库、创建美观的 XML 文档、填写持久性以对其进行压力测试，还是匿名从生产服务中获取的数据，Faker 都可以满足。

* pip 安装 faker

```shell
pip install faker
```

__使用例子__

```python
from faker import Faker

fake = Faker(locale='zh_CN')

# 基本常用数据
name = fake.name()
address = fake.address()
phone = fake.phone_number()
ID = fake.ssn(min_age=18)

print(f"""
    name: {name},
    address: {address}, 
    phone: {phone}, 
    ID: {ID}""")

# 日期时间相关
day_of_month = fake.day_of_month()
day_of_week = fake.day_of_week()
date = fake.date(pattern="%Y-%m-%d")
date_between = fake.date_between(start_date="-30y", end_date="today")
future_datetime = fake.future_datetime(end_date="+30d",)
past_datetime = fake.past_datetime(start_date="-30d", )

print(f"""
    day_of_month: {day_of_month},
    day_of_week: {day_of_week},
    data: {date},
    date_between: {date_between},
    future_datetime: {future_datetime},
    past_datetime: {past_datetime}""")

# 网络相关
email = fake.ascii_free_email()
domain = fake.domain_name(levels=1)
host = fake.hostname()
image_url = fake.image_url()
url = fake.url()
uri = fake.uri()
ipv4 = fake.ipv4(network=False)
ipv6 = fake.ipv6(network=False)

print(f"""
    email: {email},
    domain: {domain},
    host: {host},
    image_url: {image_url},
    url: {url},
    uri: {uri},
    ipv4: {ipv4},
    ipv6: {ipv6}""")

```

__代码说明__

faker提供的方法太多了，夸张点可以用`只有你想不到，没有他做不到`来形容，例子给出了一些比较常用的数据。


__执行结果__

```shell
> python faker_sample.py

    name: 田凤兰,
    address: 江苏省桂香县房山济南路B座 619737,
    phone: 15373390812,
    ID: 421381194609238767
    
    day_of_month: 24,
    day_of_week: 星期一,
    data: 2005-01-03,
    date_between: 2020-01-04,
    future_datetime: 2022-11-29 22:49:38,
    past_datetime: 2022-11-23 17:41:18

    email: guiyingwang@yahoo.com,
    domain: 90.cn,
    host: desktop-59.guiying.cn,
    image_url: https://placeimg.com/202/816/any,
    url: https://luo.cn/,
    uri: http://www.yongsun.cn/,
    ipv4: 37.222.72.50,
    ipv6: edcb:f32:3137:478c:ee6e:35f0:d572:6ddd
```


### hypothesis

Hypothesis是Python的一个高级测试库。它允许编写测试用例时参数化，然后生成使测试失败的简单易懂的测试数据。可以用更少的工作在代码中发现更多的bug。

假说是一个测试库家族，它允许您编写通过示例源参数化的测试。然后，假设实现生成简单而可理解的示例，使您的测试失败。这简化了您的测试编写，同时使它们更强大，让软件自动化枯燥的部分，并以比人类更高的标准执行它们，使您可以专注于更高级别的测试逻辑

Hypothesis已经超出单纯生成测试数据的范围，通过他提供的方法可以构造多条测试随机数，以此简化测试用例的编写。

* pip 安装 Hypothesis

```
> pip install hypothesis
```

__使用例子__

使用hypothesis生成测试数据辅助测试。

```py
# hypothesis_sample.py
import unittest
from hypothesis import given, settings
import hypothesis.strategies as st


def add(a: int, b: int):
    """被测试函数"""
    return a + b


class AddTest(unittest.TestCase):

    @settings(max_examples=10)
    @given(a=st.integers(), b=st.integers())
    def test_case(self, a, b):
        print(f"测试数据：a-> {a}, b-> {b}")
        c2 = add(a, b)
        self.assertIsInstance(c2, int)


if __name__ == '__main__':
    unittest.main()
```

__代码说明__

在 `@settings()`装饰器中，通过max_examples 参数设置最大生成几组测试数据。

通过`@given()`装饰测试用例，调用strategies 模块下面的 integers() 方法生成随机的测试数。


__执行结果__

```
> python hypothesis_sample.py

测试数据：a-> 0, b-> 0
测试数据：a-> 0, b-> 0
测试数据：a-> 0, b-> 0
测试数据：a-> 7669, b-> 4446534194746394334
测试数据：a-> 0, b-> 0
测试数据：a-> 0, b-> 0
测试数据：a-> -27312, b-> 0
测试数据：a-> -27312, b-> 26593
测试数据：a-> 29942, b-> 0
测试数据：a-> 29942, b-> 30648
.
----------------------------------------------------------------------
Ran 1 test in 0.010s

OK
```

通过测试结果可以看到，随机生成10组数据验证被测试的add()函数。

> 这种测试通常被称为“基于属性的测试”，这个概念最广为人知的实现是Haskell库QuickCheck，但hypothesis与QuickCheck有很大的不同，它被设计成习惯地、容易地适应您所习惯的现有测试风格，而您完全不需要熟悉Haskell或函数编程。

在使用hypothesis的时候，我们一定要明确他的特点：

1. 虽然生成了10条数据，但被记录为一条用例，所以，10条数据的任何一条数据都有可能导致用例失败。
2. 因为数据是随机生成的，所以重复执行并不能复现上次失败的问题。
3. 随机数据导致无法预判被测试函数返回的结果，所以，我们只能从类型或范围上编写断言。

