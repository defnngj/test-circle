from webdriver_chinning import Steps

def test_case1():
    """百度搜索"""
    Steps(url="https://www.baidu.com").open().sleep(2).find("#kw").type("selenium").find("#su").click().close()


def test_case2():
    """百度搜索"""
    s = Steps(url="https://www.baidu.com")
    s.open().sleep(2)
    s.find("#kw").type("selenium")
    s.find("#su").click()
    s.close()


def test_case3():
    """百度搜索设置"""
    Steps(url="http://www.baidu.com")\
            .open()\
            .find("#s-usersetting-top").click()\
            .find("#s-user-setting-menu > div > a.setpref").click().sleep(2)\
            .find('[data-tabid="advanced"]').click().sleep(2)\
            .find("#q5_1").click().sleep(2)\
            .find('[data-tabid="general"]').click().sleep(2)\
            .find("text=保存设置").click()\
            .alert().accept()\
            .close()


