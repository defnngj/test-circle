from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class Page:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    @property
    def search_input(self):
        return self.driver.find_element(By.ID, "kw")

    @property
    def search_button(self):
        return self.driver.find_element(By.ID, "su")


class BotPage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def type_search_input(self, text):
        self.driver.find_element(By.ID, "kw").send_keys(text)

    def click_search_button(self):
        self.driver.find_element(By.ID, "su").click()
