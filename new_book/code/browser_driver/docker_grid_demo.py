from selenium.webdriver import Remote, DesiredCapabilities

# 引用firefox浏览器配置
driver = Remote(command_executor='http://localhost:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.FIREFOX.copy())

driver.get("https://www.bing.com")
search = driver.find_element("id", "sb_form_q")
search.send_keys("docker-selenium")
search.submit()
