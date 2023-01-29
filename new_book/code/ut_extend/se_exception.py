from  selenium import webdriver

dr = webdriver.Chrome()
dr.get("http://www.bing.com")
dr.find_element_by_id("xxx")
