import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


def hello_world():
    browser = webdriver.Chrome()
    browser.get('http://www.baidu.com/')
    search_box = browser.find_element(By.ID, "kw")
    search_box.send_keys('seldom')
    search_box.send_keys(Keys.ENTER)


def main():
    hello_world()


if __name__ == '__main__':
    start = time.time()
    main()
    print("running time:", time.time() - start)
