# hybrid_style.py
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class BingPage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def search_input(self, text="", enter=False):
        elem = self.driver.find_element(By.ID, "sb_form_q")
        elem.clear()
        elem.send_keys(text)
        if enter is True:
            elem.submit()

    def search_icon(self):
        self.driver.find_element(By.ID, "search_icon").click()
