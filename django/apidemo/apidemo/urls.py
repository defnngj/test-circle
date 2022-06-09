"""apidemo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib import auth
from ninja import NinjaAPI
from ninja import Schema

api = NinjaAPI()


class LoginIn(Schema):
    username: str
    password: str


@api.post("/login")
def user_login(request, payload: LoginIn):
    """
    用户登录
    """
    user = auth.authenticate(username=payload.username, password=payload.password)
    if user is not None:
        return {"success": True, "msg": "login success"}
    else:
        return {"success": False, "msg": "login fail"}


urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", api.urls),
]
