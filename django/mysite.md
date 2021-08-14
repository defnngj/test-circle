## django 官方例子之投票系统

django作为一个诞生于2003年的的Python Web框架，有着悠久的历史。以前做Python Web开发，我们时常会拿他和Flask对比，他们分别代表两个风格，Flask代表小而美，Django代表大而全。随着sanic、fastapi的兴起，他们都走了Flask框架的风格。因为更好的支持异步，所以，在性能评测中Django是经常被拿出来吊打的那个。那个django真的是否已经过时了呢？我最近实现一个完整系统的后端服务时，分别尝试用fastapi 和 django + django-rest-framework，发现后者其实更方便。


### django很简单

为什么我会认为django很简单。

* ORM

Django自带的ORM非常简单好用，django默认使用sqlit3，这个东西让我一度忽视了原来Web框架还是需要考虑数据连接和表设计的。对于初学Python Web框架的同学，只需要需掌握简单的ORM用法就可以愉快的操作数据库了。
```py
from polls.models import Question

# 查询 id=2的 question
Question.objects.get(id=2)
```

* 自带一些常用表

比如用户组表、用户表、session表等，我要实现一个系统最简单的登录注册，压根都不需要自己设计表结构，django一条命令就我们生成好了，配合Django提供的API，可以说几行代码实现一个登录、注册。密码还自动在数据库加密的啊，又省去了学习md5、base64 的用法。

![](/django/django_sqlite.png)

* Admin后台

不需要编写一行代码你将拥有一个管理后台，然后，只需要几行代码，就可以将你的表注册到Admin后台，实现曾删查改的Web功能。

![](/django/django_admin.png)

* django-rest-framework

当我尝试用django编写后端接口时，django-rest-framework简直是神器，当然，它的过度封装确实有利有弊，而且入门还不小的门槛。但它自带的各种认证也非常强大，作为一个后端服务，接口认证肯定是必要的，而django-rest-framework这方面简单配置即可实现。

```py
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    你能相信这个类已经实现了User的增删查改吗？
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
```


## django很复杂

* 入门难

看看flask/fastapi的官方文档，一个demo几行代码就跑起来了；而django又要创建项目(mysite)，又要创建应用(polls)，还需要配置文件(stting.py)，还需要指定路由文件(urls.py)、还需要编写视图文件(view.py)，还有一大堆不知道干嘛的文件。

```py
# fastapi demo
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

django 项目

```shell

mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        asgi.py
        wsgi.py
    polls/
        __init__.py
        admin.py
        apps.py
        migrations/
            __init__.py
        models.py
        tests.py
        views.py
```

* 实现逻辑很复杂

看看fastapi 再带入参类型校验，返回数据直接支持字典， django对拿过来的参数又判断None，又判断类型、长度，不有各种 Response，但是，如果配合使用django-rest-framework，那就要多简洁就多简洁。


## django视频

django官方的投票系统就是很好的入门教程，我将他录制成了视频放到了B站，如果需要学习django框架的同学直接拿去。

https://www.bilibili.com/video/BV1oq4y1W7ym

