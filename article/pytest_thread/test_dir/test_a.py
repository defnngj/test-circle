import time
from selenium import webdriver


def test_01():
    driver = webdriver.Chrome()
    driver.get("http://www.baidu.com")
    elem = driver.find_element_by_id("kw")
    elem.send_keys("unittest")
    elem.submit()
    time.sleep(2)
    assert driver.title == "unittest_百度搜索"
    driver.quit()


def test_02():
    driver = webdriver.Chrome()
    driver.get("http://www.baidu.com")
    elem = driver.find_element_by_id("kw")
    elem.send_keys("python")
    elem.submit()
    time.sleep(2)
    assert driver.title == "python_百度搜索"
    driver.quit()

