from selenium.webdriver.remote.webdriver import WebDriver
from seleniumpagefactory.Pagefactory import PageFactory


class BingPage(PageFactory):

    def __init__(self, driver: WebDriver):
        # It is necessary to to initialise driver as page class member to implement Page Factory
        self.driver = driver

    # define locators dictionary where key name will became WebElement using PageFactory
    locators = {
        "searchInput": ('ID', 'sb_form_q'),
        "searchIcon": ('NAME', 'search_icon'),
        "searchResult": ('XPATH', '//h2/a/i')
    }

    def search(self):
        # set_text(), click_button() methods are extended methods in PageFactory
        self.searchInput.set_text("selenium-page-factory")  # edtUserName become class variable using PageFactory
        self.searchIcon.click_button()

    def search_result(self):
        # 搜索结果
        return self.searchResult
