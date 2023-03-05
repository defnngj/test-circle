from time import sleep
from selenium.webdriver import Chrome
from page_object import BingPage

driver = Chrome()
driver.get("http://cn.bing.com")

# 调用BingPage类
page = BingPage(driver)
page.search_input.send_keys("bot style tests")
page.search_icon.click()

sleep(4)
driver.close()

