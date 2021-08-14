
def test_baidu_search(baidu_page, base_url):
    """
    搜索
    """
    baidu_page.get(base_url)
    baidu_page.search_input.send_keys("pytest")
    baidu_page.search_button.click()
    baidu_page.sleep(2)
    assert baidu_page.get_title == "pytest_百度搜索"

