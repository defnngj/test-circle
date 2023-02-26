from time import sleep
from appium.webdriver import Remote
from appium_lab.switch import Switch
from appium_lab.action import Action
from appium_lab.find import FindByText
from appium_lab.keyevent import KeyEvent
from appium.webdriver.common.appiumby import AppiumBy

desired_caps = {
    "deviceName": "ELS-AN00",
    "automationName": "UiAutomator2",
    "platformName": "Android",
    "appPackage": "com.meizu.flyme.flymebbs",
    "appActivity": ".ui.LoadingActivity",
    "noReset": True
}

driver = Remote(command_executor="http://127.0.0.1:4723",
                desired_capabilities=desired_caps)
sleep(2)

# 点击输入框，调起屏幕键盘
driver.find_element(AppiumBy.ID, "com.meizu.flyme.flymebbs:id/et_search").click()

# 使用key_text 输入字符串
key = KeyEvent(driver)
key.key_text("Flyme9")
sleep(9)


find = FindByText(driver)
find.find_text_view("综合讨论").click()
sleep(5)


action = Action(driver)
# 屏幕尺寸
action.size()
# 向上滑动
action.swipe_up(times=3)
# 向下滑动
action.swipe_down(times=1)
# 触摸坐标位
action.tap(x=100, y=1333)


context = Switch(driver)
# 打印并返回当前上下文
context.context()
# 切换到 webview
context.switch_to_web()
# 切换到 native
context.switch_to_app()
# 切换到 flutter
context.switch_to_flutter()
