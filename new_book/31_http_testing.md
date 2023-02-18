## http接口测试库

近几年，随着微服务在各个软件公司落地，接口测试变得尤为重要，加上接口测试本身以相对简单、稳定性好等特性，更容易实现自动化测试，所以，许多公司的测试团队会优先开展接口自动化测试。在所有项目接口中，以HTTP、RPC接口为主，其中又以HTTP接口应用最为广泛。


在python语言中有许多简单好用的HTTP测试库，例如 requests、httpx、aiohttp等。


## requests 

requests 是一个非常流行的http 客户端库。他属于是python语言下面的明星项目了，以简单、强大的API得到广泛的应用，并且被其他诸多http库提供参考。

* pip安装

```shell
pip install requests
```

__简单示例__

实现一个get接口调用，并且需要auth认证。

```py
import requests

r = requests.get('https://api.github.com/user', auth=('user', 'pass'))
print(f"返回状态码： {r.status_code}")
print(f"返回数据（JSON）： {r.json()}")
```

## httpx

httpx 定位于Python下一代http客户端， 它包括一个集成的命令行客户端，支持 HTTP/1.1 和 HTTP/2，并提供同步和异步 API。

* pip安装

```shell
pip install httpx
```

__简单示例__

httpx 有着和 requests 类似的用法，通过get请求一个页面。

```py
import httpx

r = httpx.get('https://www.example.org/')
print(f"状态码： {r.status_code}")
print(f"返回数据： {r.text}")
```

httpx 同样支持异步的调用。

```py
import asyncio
import httpx


async def main():
    async with httpx.AsyncClient() as client:
        r = await client.get('https://www.example.com/')
        print(f"状态码： {r.status_code}")
        print(f"返回数据： {r.text}")

asyncio.run(main())
```

## aiohttp

aiohttp 是一款支持异步的 http 客户端/服务端 框架。同时还支持 Web-Sockets 协议。

* pip安装

```shell
pip install aiohttp
```

__简单示例__

异步实现一个http客户端请求。

```py
import aiohttp
import asyncio

async def main():

    async with aiohttp.ClientSession() as session:
        async with session.get('http://python.org') as response:

            print("Status:", response.status)

            html = await response.text()
            print("Body:", html[:15], "...")

asyncio.run(main())
```

异步实现一个 http 服务。

```py
# aiohttp_server.py
from aiohttp import web


async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle)])

if __name__ == '__main__':
    web.run_app(app)

```

启动服务

```
> python aiohttp_server.py
======== Running on http://0.0.0.0:8080 ========
(Press CTRL+C to quit)
```

通过浏览器访问：

```
http://127.0.0.1:8080/tom
```
你将会在页面中看到：

Hello, tom

