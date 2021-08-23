from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By


class ActionBot:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def click(self, *locator):
        self.driver.find_element(*locator).click()

    def submit(self, *locator):
        self.driver.find_element(*locator).submit()

    def type(self, *locator, text):
        elem = self.driver.find_element(*locator)
        elem.clear()
        elem.send_keys(text)


class BotPage(ActionBot):

    def type_search_input(self, text):
        self.type(*(By.ID, "kw"), text=text)

    def click_search_button(self):
        self.click(By.ID, "su")
