# poium_page.py
from poium import Page, Element, Elements


class BingPage(Page):
    """bing 搜索页面"""
    search_input = Element(id_="sb_form_q", describe="bing搜索输入框", timeout=3)
    search_icon = Element(id_="search_icon", describe="bing搜索输入框", timeout=1)
    search_search = Elements(xpaht="//h2/a", describe="搜索结果", timeout=5)
