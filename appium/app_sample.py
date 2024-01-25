from appium import webdriver
from time import sleep


# 定义运行环境
desired_caps = {
    'deviceName': 'JEF_AN20',
    'automationName': 'appium',
    'platformName': 'Android',
    'platformVersion': '10.0',
    'appPackage': 'com.meizu.flyme.flymebbs',
    'appActivity': '.ui.LoadingActivity',
    'noReset': True,
    'ignoreHiddenApiPolicyError': True
}

# 启动App
dr = webdriver.Remote(
    command_executor='http://127.0.0.1:4723/wd/hub',
    desired_capabilities=desired_caps)

sleep(2)

# 通过图片定位元素
dr.find_element_by_image(r"D:\appium\image\write.png").click()
