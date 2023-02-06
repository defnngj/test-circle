from selenium.webdriver import Chrome
from common.case import TestCase
from common.case import Browser
from common.case import main


class MyTest(TestCase):

    def setUp(self) -> None:
        Browser.driver = Chrome()

    def tearDown(self) -> None:
        Browser.driver.quit()

    def test_case(self):
        Browser.driver.get("https://www.selenium.dev/")
        self.assertTitle("Selenium")
        self.assertInTitle("Se")
        self.assertUrl("https://www.selenium.dev/")
        self.assertInText("Selenium automates browsers. That's it!")


if __name__ == '__main__':
    main()
