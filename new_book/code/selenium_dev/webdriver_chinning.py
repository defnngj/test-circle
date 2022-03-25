# coding=utf-8
import time
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


__all__ = ["Steps"]


class Selenium:
    driver = None   # 定义驱动
    element = None  # 定义元素
    alert = None    #


class Steps(object):
    """
    Webdriver Basic method chaining
    Write test cases quickly.
    """

    def __init__(self, url: str = None):
        Selenium.driver = Chrome()  # 默认浏览器
        self.url = url

    def open(self, url: str = None):
        """
        open url.

        Usage:
            open("https://www.baidu.com")
        """
        if self.url is not None:
            Selenium.driver.get(self.url)
        else:
            Selenium.driver.get(url)
        return self

    def find(self, css: str, index: int = 0):
        """
        find element
        """
        if len(css) > 5 and css[:5] == "text=":
            web_elem = Selenium.driver.find_elements(By.LINK_TEXT, css[5:])[index]
        elif len(css) > 6 and css[:6] == "text*=":
            web_elem = Selenium.driver.find_elements(By.PARTIAL_LINK_TEXT, css[6:])[index]
        else:
            web_elem = Selenium.driver.find_elements(By.CSS_SELECTOR, css)[index]
        Selenium.element = web_elem
        return self

    def type(self, text):
        """
        type text.
        """
        Selenium.element.send_keys(text)
        return self

    def click(self):
        """
        click.
        """
        Selenium.element.click()
        return self

    def clear(self):
        """
        clear input.
        Usage:
            clear()
        """
        Selenium.element.clear()
        return self

    def submit(self):
        """
        submit input
        Usage:
            submit()
        """
        Selenium.element.submit()
        return self

    def enter(self):
        """
        enter.
        Usage:
            enter()
        """
        Selenium.element.send_keys(Keys.ENTER)
        return self

    def close(self):
        """
        Closes the current window.

        Usage:
            close()
        """
        Selenium.driver.close()
        return self

    def quit(self):
        """
        Quit the driver and close all the windows.

        Usage:
            quit()
        """
        Selenium.driver.quit()

    def alert(self):
        """
        get alert.
        Usage:
            alert()
        """
        Selenium.alert = Selenium.driver.switch_to.alert
        return self

    def accept(self):
        """
        Accept warning box.

        Usage:
            alert().accept()
        """
        Selenium.alert.accept()
        return self

    def dismiss(self):
        """
        Dismisses the alert available.

        Usage:
            alert().dismiss()
        """
        Selenium.driver.switch_to.alert.dismiss()
        return self

    def select(self, value: str = None, text: str = None, index: int = None):
        """
        Constructor. A check is made that the given element is, indeed, a SELECT tag. If it is not,
        then an UnexpectedTagNameException is thrown.
        """
        elem = Selenium.element
        if value is not None:
            Select(elem).select_by_value(value)
        elif text is not None:
            Select(elem).select_by_visible_text(text)
        elif index is not None:
            Select(elem).select_by_index(index)
        else:
            raise ValueError(
                '"value" or "text" or "index" options can not be all empty.')
        return self

    def sleep(self, sec: int):
        """
        Usage:
            sleep(seconds)
        """
        time.sleep(sec)
        return self
