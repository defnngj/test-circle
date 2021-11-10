import time
from selenium import webdriver


def test_03():
    driver = webdriver.Chrome()
    driver.get("https://www.bing.com/?mkt=zh-CN")
    elem = driver.find_element_by_id("sb_form_q")
    elem.send_keys("多线程")
    elem.submit()
    time.sleep(2)
    assert "多线程" in driver.title
    driver.quit()
