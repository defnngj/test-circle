import time
import asyncio
from playwright.async_api import async_playwright

async def hello_world():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()
        await page.goto("http://www.baidu.com")
        await page.fill('#kw', "playwright")
        await page.click('#su')
        await browser.close()

def main():
    asyncio.run(hello_world())


if __name__ == '__main__':
    start = time.time()
    main()
    print("running time:", time.time() - start)