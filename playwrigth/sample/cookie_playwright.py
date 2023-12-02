import os
import asyncio
from playwright.async_api import async_playwright

WEB_DIR = os.path.dirname(os.path.abspath(__file__))
COOKIE_PATH = os.path.join(WEB_DIR, "cookie.json")


async def main():
    async with async_playwright() as p:
        print("open browser")
        browser = await p.chromium.launch(headless=False)
        # 3.读取本地登录cookie
        context = await browser.new_context(storage_state=COOKIE_PATH)
        page = await context.new_page()
        await page.goto('https://www.baidu.com')
        # # 1.打断点
        # await page.pause()
        # # 2. 将登录之后的cookie保存到本地
        # storage = await context.storage_state(path=COOKIE_PATH)
        # print(storage)
        # await page.screenshot(path=f'example.png')
        await browser.close()
        print("close browser")


if __name__ == '__main__':
    asyncio.run(main())
