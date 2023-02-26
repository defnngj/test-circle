# appium_android.py
from time import sleep
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy


# Android App配置
desired_caps = {
    "deviceName": "ELS-AN00",
    "automationName": "UiAutomator2",
    "platformName": "Android",
    "appPackage": "com.meizu.flyme.flymebbs",
    "appActivity": ".ui.LoadingActivity",
    "noReset": True,
}

driver = webdriver.Remote(command_executor="http://127.0.0.1:4723",
                          desired_capabilities=desired_caps)
sleep(2)

# 搜索 flyme 关键字
driver.find_element(MobileBy.ID, "com.meizu.flyme.flymebbs:id/nw").click()
sleep(2)
driver.find_element(MobileBy.ID, "com.meizu.flyme.flymebbs:id/nw").send_keys("flyme")
driver.find_element(MobileBy.ID, "com.meizu.flyme.flymebbs:id/o1").click()
sleep(2)

# 打印结果列表
title_list = driver.find_elements(MobileBy.ID, "com.meizu.flyme.flymebbs:id/a29")
for title in title_list:
    print(title.text)

# 关闭App
driver.quit()
