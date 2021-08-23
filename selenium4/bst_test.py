import time
from selenium.webdriver.common.by import By
from bst import ActionBot, BotPage
from po import Page, BotPage


def test_bst(browser):
    browser.get("http://www.baidu.com")
    action_bot = ActionBot(browser)
    action_bot.type(*(By.ID, "kw"), text="bot style tests")
    action_bot.click(*(By.ID, "su"))
    time.sleep(5)


def test_po(browser):
    browser.get("http://www.baidu.com")
    page = Page(browser)
    page.search_input.send_keys("bot style tests")
    page.search_button.click()


def test_bst_po(browser):
    browser.get("http://www.baidu.com")
    page = BotPage(browser)
    page.type_search_input("bot style tests")
    page.click_search_button()

