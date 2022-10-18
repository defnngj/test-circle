# playwright 定位器

https://playwright.dev/python/docs/locators

https://playwright.dev/docs/selectors


元素定位非常重要，他是操作元素的前提。playwright提供`locator()` 来实现元素的定位。

## playwright选择器

__重点:__

* id
* text
* [css **](https://www.w3school.com.cn/cssref/css_selectors.asp)
* [xpath](https://www.w3school.com.cn/xpath/xpath_syntax.asp)

__例子:__

* Text selector

```py
page.locator("text=Log in").click()
```

* CSS selector

```py
page.locator("button").click()
page.locator("#nav-bar .contact-us-item").click()
```

* Select by attribute, with css selector

```py
page.locator("[data-test=login-button]").click()
page.locator("[aria-label='Sign in']").click()
```


* Combine css and text selectors

```py
page.locator("article:has-text('Playwright')").click()
page.locator("#nav-bar :text('Contact us')").click()
```

* Element that contains another, with css selector

```py
page.locator(".item-description:has(.item-promo-banner)").click()

```

* Selecting based on layout, with css selector

```py
page.locator("input:right-of(:text('Username'))").click()
```


* Only visible elements, with css selector

```py
page.locator(".login-button:visible").click()
```


* Pick n-th match

```py
page.locator(":nth-match(:text('Buy'), 3)").click()
```

* XPath selector

```py
page.locator("xpath=//button").click()
```


* React selector (experimental)

```py
page.locator("_react=ListItem[text *= 'milk' i]").click()
```


* Vue selector (experimental)

```py
page.locator("_vue=list-item[text *= 'milk' i]").click()
```



